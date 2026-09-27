/*
 * ======================================================================================
 * PROYECTO: EduOrden IA - Casilleros Inteligentes con Visión Computacional
 * DISPOSITIVO: ESP32-CAM (AI-Thinker)
 * DESCRIPCIÓN: 
 *   - Lee sensor infrarrojo de presencia en el casillero.
 *   - Captura una imagen con la cámara OV2640.
 *   - Envía la fotografía mediante HTTP POST a un servidor local de IA (Python).
 *   - Recibe la respuesta (JSON con clase detectada y coincidencia).
 *   - Activa señales visuales (LEDs / Neopixel) y acústicas (DFPlayer Mini / Buzzer).
 * ======================================================================================
 */

#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// ======================== CREDENCIALES WI-FI ========================
// Conectar a la red local del computador/laptop del expositor
const char* WIFI_SSID     = "EduOrden_RedLocal";
const char* WIFI_PASSWORD = "claveSegura123";

// URL del servidor local de inferencia (Python Flask / FastAPI)
// Reemplazar con la IP local de tu computador (ejecuta 'ipconfig' en Windows)
const char* SERVER_URL    = "http://192.168.1.100:5000/predecir";

// Identificador del casillero donde está instalada o enfocada esta cámara
const char* CASILLERO_ID  = "casillero_1"; // Casillero destinado a "cuaderno"

// =================== ASIGNACIÓN DE PINES ESP32-CAM ===================
// Pines estándar de la placa AI-THINKER ESP32-CAM
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// Pines para periféricos (Nota: usar pines libres que no interfieran con la cámara)
const int PIN_SENSOR_IR     = 13; // Entrada digital: Sensor IR de presencia (TCRT5000)
const int PIN_LED_FLASH     = 4;  // Flash interno de la ESP32-CAM para iluminación
const int PIN_INDICADOR_OK  = 12; // Salida digital: Luz verde / Actuador Éxito
const int PIN_INDICADOR_TRY = 14; // Salida digital: Luz ámbar / Actuador Reintento
const int PIN_TRIGGER_AUDIO = 15; // Salida hacia pin de disparo de audio o DFPlayer

// Variables de estado
bool objetoDetectadoAnterior = false;
unsigned long ultimoTiempoCaptura = 0;
const unsigned long DEBOUNCE_TIEMPO = 2000; // 2 segundos entre capturas para evitar dobles disparos

// =================== INICIALIZACIÓN DE LA CÁMARA ===================
bool configurarCamara() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_siod     = SIOD_GPIO_NUM;
  config.pin_sioc     = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // Optimización de resolución y compresión para transmisión rápida
  if(psramFound()){
    config.frame_size   = FRAMESIZE_VGA;  // 640x480 con PSRAM
    config.jpeg_quality = 12;             // 10 a 63 (menor número = mejor calidad)
    config.fb_count     = 2;
  } else {
    config.frame_size   = FRAMESIZE_QVGA; // 320x240 sin PSRAM
    config.jpeg_quality = 16;
    config.fb_count     = 1;
  }

  // Iniciar el periférico de cámara
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Error al iniciar cámara: 0x%x\n", err);
    return false;
  }

  // Ajustes de sensor para interior de casillero
  sensor_t * s = esp_camera_sensor_get();
  s->set_brightness(s, 1);    // Incrementar ligeramente el brillo (+1)
  s->set_contrast(s, 1);      // Mayor contraste para bordes claros
  s->set_saturation(s, 0);
  s->set_whitebal(s, 1);      // Balance de blancos automático
  return true;
}

// =================== CONEXIÓN WI-FI ===================
void conectarWiFi() {
  Serial.print("Conectando a Wi-Fi: ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 25) {
    delay(500);
    Serial.print(".");
    intentos++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[Wi-Fi] Conexión establecida con éxito.");
    Serial.print("[Wi-Fi] Dirección IP asignada: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[Wi-Fi] No se pudo conectar. Operando en modo de espera.");
  }
}

// =================== ENVÍO DE FOTO AL SERVIDOR ===================
void capturarYEnviarImagen() {
  Serial.println("\n[Acción] Sensor activado: capturando imagen...");

  // Encender suavemente el flash de iluminación si está disponible
  digitalWrite(PIN_LED_FLASH, HIGH);
  delay(150); // Tiempo para estabilización de luz

  // Capturar buffer de imagen
  camera_fb_t * fb = esp_camera_fb_get();
  digitalWrite(PIN_LED_FLASH, LOW); // Apagar flash inmediatamente

  if (!fb) {
    Serial.println("[Error] Falló la captura del fotograma.");
    return;
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[Aviso] Wi-Fi desconectado. Intentando reconectar...");
    WiFi.reconnect();
    esp_camera_fb_return(fb);
    return;
  }

  HTTPClient http;
  String fullUrl = String(SERVER_URL) + "?casillero=" + String(CASILLERO_ID);
  http.begin(fullUrl);
  http.addHeader("Content-Type", "image/jpeg");
  http.setTimeout(4000); // 4 segundos de timeout máximo

  Serial.println("[Red] Transmitiendo imagen al servidor de IA...");
  int httpResponseCode = http.POST(fb->buf, fb->len);

  if (httpResponseCode > 0) {
    String payload = http.getString();
    Serial.printf("[Servidor] Código HTTP: %d | Respuesta: %s\n", httpResponseCode, payload.c_str());
    
    // Evaluar la respuesta recibida del servidor
    // Ejemplo de respuesta esperada: {"resultado":"CORRECTO","clase":"cuaderno","confianza":0.95}
    if (payload.indexOf("\"resultado\":\"CORRECTO\"") >= 0 || payload.indexOf("CORRECTO") >= 0) {
      ejecutarRetroalimentacionExito();
    } else if (payload.indexOf("\"resultado\":\"INCORRECTO\"") >= 0 || payload.indexOf("INCORRECTO") >= 0) {
      ejecutarRetroalimentacionReintento();
    } else {
      Serial.println("[Info] Objeto no reconocido con suficiente certeza.");
      ejecutarRetroalimentacionDuda();
    }
  } else {
    Serial.printf("[Error HTTP] Código de error en la petición: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  esp_camera_fb_return(fb); // Liberar memoria del framebuffer
}

// =================== RESPUESTAS MULTISENSORIALES ===================
void ejecutarRetroalimentacionExito() {
  Serial.println("[Feedback] >>> ¡ACIERTO! Objeto correcto en su casillero <<<");
  digitalWrite(PIN_INDICADOR_OK, HIGH);
  digitalWrite(PIN_TRIGGER_AUDIO, HIGH);
  delay(100);
  digitalWrite(PIN_TRIGGER_AUDIO, LOW); // Pulso para disparar pista de éxito en DFPlayer

  delay(2500); // Mantener luz verde encendida
  digitalWrite(PIN_INDICADOR_OK, LOW);
}

void ejecutarRetroalimentacionReintento() {
  Serial.println("[Feedback] >>> REINTENTO: El objeto no corresponde <<<");
  // Parpadeo suave y pausado (no alarmante ni estridente)
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_INDICADOR_TRY, HIGH);
    delay(300);
    digitalWrite(PIN_INDICADOR_TRY, LOW);
    delay(200);
  }
}

void ejecutarRetroalimentacionDuda() {
  Serial.println("[Feedback] >>> IMAGEN NO CLARA: Reacomodar objeto <<<");
  digitalWrite(PIN_INDICADOR_TRY, HIGH);
  delay(600);
  digitalWrite(PIN_INDICADOR_TRY, LOW);
}

// =================== SETUP & LOOP ===================
void setup() {
  Serial.begin(115200);
  Serial.println("\n--- Iniciando EduOrden IA (ESP32-CAM) ---");

  pinMode(PIN_SENSOR_IR, INPUT);
  pinMode(PIN_LED_FLASH, OUTPUT);
  pinMode(PIN_INDICADOR_OK, OUTPUT);
  pinMode(PIN_INDICADOR_TRY, OUTPUT);
  pinMode(PIN_TRIGGER_AUDIO, OUTPUT);

  digitalWrite(PIN_LED_FLASH, LOW);
  digitalWrite(PIN_INDICADOR_OK, LOW);
  digitalWrite(PIN_INDICADOR_TRY, LOW);
  digitalWrite(PIN_TRIGGER_AUDIO, LOW);

  if (!configurarCamara()) {
    Serial.println("[Crítico] La cámara no pudo inicializarse. Reiniciando...");
    delay(3000);
    ESP.restart();
  }

  conectarWiFi();
  Serial.println("[Listo] Sistema esperando interacción de usuario en el casillero.");
}

void loop() {
  // Lectura del sensor de proximidad del casillero (activo en nivel bajo o alto según modelo)
  // LOW significa detección en sensores habituales TCRT5000
  int lecturaIR = digitalRead(PIN_SENSOR_IR);
  bool objetoPresente = (lecturaIR == LOW);

  unsigned long tiempoActual = millis();

  // Flanco de subida: el niño acaba de colocar el objeto y se cumple el tiempo de debounce
  if (objetoPresente && !objetoDetectadoAnterior && (tiempoActual - ultimoTiempoCaptura > DEBOUNCE_TIEMPO)) {
    ultimoTiempoCaptura = tiempoActual;
    delay(400); // Pequeña pausa para que la mano del niño se retire y el objeto quede inmóvil
    capturarYEnviarImagen();
  }

  objetoDetectadoAnterior = objetoPresente;
  delay(50);
}
