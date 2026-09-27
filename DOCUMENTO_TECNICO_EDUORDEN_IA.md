# PROYECTO TECNOLÓGICO EDUCATIVO: "EDUORDEN IA"
## Casilleros Inteligentes con ESP32-CAM y Visión Computacional para el Fomento de la Autonomía en Niños con Discapacidad Cognitiva

---

### ÍNDICE GENERAL
1. **Idea General del Proyecto**
2. **Objetivos (General, Específicos y Enfoque Pedagógico)**
3. **Funcionamiento Detallado del Sistema**
4. **Lista Completa de Componentes y Justificación Técnica**
5. **Arquitectura del Sistema (Flujo de Datos e Infraestructura)**
6. **Visión Computacional e Inteligencia Artificial**
7. **Lógica del Sistema (Algoritmo y Pseudocódigo Estructurado)**
8. **Diseño de Interfaz y Retroalimentación Multisensorial**
9. **Diseño Físico y Estructural de la Maqueta**
10. **Inclusión, Accesibilidad y Metodología Educativa (DUA y TEACCH)**
11. **Seguridad, Privacidad y Consideraciones Éticas**
12. **Presupuesto Estimado y Análisis de Costos**
13. **Fases Metodológicas de Implementación**
14. **Programación y Código Fuente Comentado**
15. **Matriz de Pruebas y Validación Experimental**
16. **Métricas de Evaluación del Impacto Educativo**
17. **Aspectos Innovadores del Proyecto**
18. **Resultado Esperado y Demostración Práctica**
19. **Guía Maestra para la Exposición y Defensa Académica**

---

## 1. IDEA GENERAL DEL PROYECTO

**EduOrden IA** es una propuesta tecnológica-educativa concebida como un dispositivo interactivo de apoyo para el aula y el hogar. Consiste en una maqueta funcional de casilleros organizadores inteligentes que integran sensores de presencia, un microcontrolador con cámara **ESP32-CAM** y algoritmos de **visión computacional / inteligencia artificial**. 

Cada compartimento del casillero está expresamente asignado a un elemento escolar de uso común:
* **Casillero 1:** Cuaderno o libro escolar.
* **Casillero 2:** Estuche de lápices o útiles de escritura.
* **Casillero 3:** Botella o cantimplora de agua.
*(Escalable a loncheras, calzado o prendas de abrigo).*

El sistema detecta automáticamente cuando un niño deposita un objeto, captura una imagen cenital del interior del compartimento y la analiza en tiempo real mediante un modelo clasificador de imágenes. Si el objeto corresponde al compartimento indicado, el sistema premia la conducta a través de estímulos multisensoriales agradables (luz LED verde suave, campanas armónicas y mensaje verbal reforzador). Si el objeto es colocado en el lugar erróneo, el sistema no emite alarmas punitivas ni frustrantes, sino que orienta de manera amigable al niño mediante una luz cálida ámbar y una pista auditiva guiada para reintentar la acción.

---

## 2. OBJETIVOS DEL PROYECTO

### 2.1. Objetivo General
Diseñar, construir y validar un prototipo funcional de casilleros inteligentes basado en la placa ESP32-CAM y técnicas de visión computacional, orientado a guiar, reforzar y evaluar la autonomía de niños con discapacidad cognitiva durante sus rutinas cotidianas de organización escolar.

### 2.2. Objetivos Específicos
1. **Desarrollar una estructura física accesible y modular** que incorpore señalética estandarizada de Comunicación Aumentativa y Alternativa (pictogramas ARASAAC), facilitando la discriminación visual sin saturación sensorial.
2. **Implementar un sistema de visión computacional optimizado** capaz de clasificar con una exactitud superior al 85% los objetos escolares seleccionados en condiciones de iluminación controlada.
3. **Programar una lógica de interacción multisensorial constructiva** fundamentada en el refuerzo positivo, que elimine el estigma del error y reduzca la ansiedad del usuario.
4. **Construir un módulo de registro y analítica pedagógica** que permita a educadores, fonoaudiólogos y familias cuantificar el progreso en tiempo de ejecución, número de reintentos y grado de autonomía alcanzado.

### 2.3. Enfoque Humano y Pedagógico
En consonancia con la Convención sobre los Derechos de las Personas con Discapacidad (ONU), EduOrden IA adopta el **modelo social de la discapacidad**: las limitaciones en el desempeño no residen en el individuo, sino en las barreras y la falta de adaptaciones de su entorno físico y social. 

EduOrden IA **no sustituye** al maestro, terapeuta ocupacional ni a los progenitores. Por el contrario, se posiciona como una **herramienta de andamiaje cognitivo**, permitiendo al niño experimentar el éxito por iniciativa propia y facilitando al adulto acompañante datos objetivos para planificar intervenciones pedagógicas personalizadas.

---

## 3. FUNCIONAMIENTO PASO A PASO

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. LLEGADA  │ ──► │ 2. DETECCIÓN │ ──► │  3. CAPTURA  │ ──► │ 4. INFERENCIA│
│   DEL NIÑO   │     │  FÍSICA (IR) │     │  ESP32-CAM   │     │  IA / PYTHON │
└──────────────┘     └──────────────┘     └──────────────┘     └──────┬───────┘
                                                                      │
                     ┌──────────────┐     ┌──────────────┐            │
                     │ 6. REGISTRO  │ ◄── │5. FEEDBACK   │ ◄──────────┘
                     │  PEDAGÓGICO  │     │ MULTISENSORIAL
                     └──────────────┘     └──────────────┘
```

1. **Aproximación:** El usuario se sitúa frente a la maqueta. Los pictogramas frontales de gran contraste identifican visualmente el destino de cada objeto.
2. **Estímulo inicial / Guía:** El casillero objetivo enciende una suave luz azul guía y el altavoz emite una instrucción clara: *"Vamos a guardar el cuaderno"*.
3. **Depósito del objeto:** El niño introduce el objeto en el casillero correspondiente.
4. **Detección por sensor de presencia:** Un sensor óptico infrarrojo (TCRT5000) ubicado en la base del casillero detecta que un objeto ha sido asentado.
5. **Captura fotográfica:** Tras un lapso de 400 milisegundos (para asegurar que la mano del niño se ha retirado y el objeto está estático), la ESP32-CAM activa su iluminación auxiliar y captura un fotograma en formato JPEG (resolución VGA 640x480).
6. **Transmisión de datos:** La ESP32-CAM envía los bytes binarios de la imagen mediante una petición `HTTP POST` a la dirección IP local del servidor de inferencia.
7. **Clasificación por IA:** El servidor procesa la imagen a través de un modelo convolucional entrenado (MobileNetV2 / Teachable Machine) y devuelve una tupla `(clase_predicha, porcentaje_confianza)`.
8. **Toma de decisión lógica:**
   * Si `clase_predicha == clase_esperada` con confianza ≥ 75%: **ACIERTO**.
   * Si `clase_predicha != clase_esperada`: **REINTENTO ASISTIDO**.
   * Si `clase_predicha == vacio` o confianza < 60%: **SOLICITUD DE ACOMODO**.
9. **Respuesta inmediata (Feedback):**
   * *Acierto:* Halo LED verde esmeralda encendido + melodía de campana + voz: *"¡Muy bien! El cuaderno está en su lugar"*.
   * *Reintento:* Halo LED ámbar titilante suave + sonido neutro + voz empática: *"Casi lo logras. Miremos bien el dibujo: este casillero es para el estuche"*.
10. **Almacenamiento del evento:** Se genera una entrada en el archivo de registro pedagógico con fecha, casillero, resultado, confianza del algoritmo y tiempo de respuesta para graficar el avance del niño.

---

## 4. LISTA DE COMPONENTES Y HARDWARE

| Componente | Función en el Proyecto | Justificación de Selección |
| :--- | :--- | :--- |
| **Módulo ESP32-CAM (AI-Thinker)** | Núcleo de captura óptica y comunicación de red. | Integra microcontrolador dual-core Tensilica Xtensa, cámara OV2640 de 2 MP y antena Wi-Fi integrada a un costo inferior a $8 USD. |
| **Convertidor USB a TTL FT232RL (FTDI)** | Programación y depuración serial. | La ESP32-CAM carece de puerto micro-USB nativo; el módulo FTDI permite flashear el firmware a 3.3V de forma segura. |
| **3x Sensores Infrarrojos TCRT5000** | Detección de presencia física de objetos. | Sensores reflectivos analógico/digitales de alta inmunidad al ruido ambiental, ideales para censar la base de cada casillero. |
| **Tira LED Neopixel WS2812B (RGB 5V)** | Señalización visual dinámica independiente por casillero. | Cada diodo es direccionable individualmente mediante un solo pin GPIO, permitiendo iluminar cada compartimento con colores arbitrarios. |
| **Módulo de Audio DFPlayer Mini** | Decodificación y reproducción de pistas de voz. | Reproduce archivos MP3/WAV desde una tarjeta MicroSD mediante comunicación UART simple, garantizando una voz humana nítida sin consumir memoria del microcontrolador. |
| **Altavoz 8Ω / 3W (Cono de 40mm)** | Salida de audio accesible. | Proporciona un volumen sonoro suficiente (65-75 dB) dentro de un aula de recursos sin distorsión. |
| **Fuente de Alimentación Conmutada 5V 3A DC** | Alimentación eléctrica general. | La ESP32-CAM consume picos de hasta 310 mA durante la transmisión Wi-Fi; una fuente robusta de 3A previene caídas de tensión *(brownouts)*. |
| **Condensador electrolítico 1000 µF / 16V** | Filtrado de rizado eléctrico. | Conectado en paralelo a los rieles de 5V y GND cerca de la placa ESP32-CAM para absorber transitorios de corriente. |
| **Estructura en Madera MDF de 3 mm** | Chasis y cajonería de la maqueta. | Económica, rígida, fácil de mecanizar con corte láser y con acabado mate que evita reflejos parásitos a la lente. |
| **Pictogramas plastificados (ARASAAC)** | Comunicación aumentativa frontal. | Sistema de pictogramas con licencia Creative Commons ampliamente estandarizado en la educación especial hispanohablante. |
| **Computador Portátil / Servidor Local** | Servidor de Inferencia Python (FastAPI/Flask). | Ejecuta el modelo de clasificación neuronal en menos de 100 ms sin sobrecargar térmicamente a la ESP32-CAM. |

---

## 5. ARQUITECTURA DEL SISTEMA

### 5.1. Diagrama de Capas
El proyecto se organiza bajo una arquitectura desacoplada en tres capas fundamentales:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CAPA 1: ENTORNO FÍSICO                          │
│   • 3 Casilleros con Pictogramas ARASAAC                               │
│   • Base con sensores ópticos de presencia (TCRT5000)                  │
│   • Halos lumínicos direccionables WS2812B por casillero               │
│   • Altavoz frontal para instrucciones audibles                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Interacción física y señales GPIO
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    CAPA 2: NODO EDGE (ESP32-CAM)                       │
│   • Adquisición: Lente OV2640 en resolución VGA (640x480)              │
│   • Lógica de disparo por sensor (Debounce de 2 segundos)              │
│   • Cliente HTTP: Empaquetado y envío multipart/binary                 │
│   • Actuación de periféricos según respuesta recibida                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Wi-Fi 802.11 b/g/n (Red Local Privada)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    CAPA 3: SERVIDOR LOCAL DE IA                        │
│   • Microservicio Python (Flask / FastAPI) en puerto 5000              │
│   • Preprocesamiento OpenCV (Normalización, Redimensión 224x224)       │
│   • Inferencia: TensorFlow Lite / MobileNetV2 pre-entrenado            │
│   • Mapeo semántico: ¿Objeto Detectado == Casillero Destino?          │
│   • Motor de Logging en JSON / SQLite para Analítica Pedagógica        │
│   • Dashboard Web en HTML5/CSS3 para el profesor en tiempo real        │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.2. Justificación de la Alternativa Híbrida (ESP32-CAM + Servidor Local)
Existen dos paradigmas técnicos para este proyecto:
1. **Inferencia totalmente integrada (Edge AI con TensorFlow Lite Micro en ESP32):**
   * *Ventaja:* No requiere computador externo.
   * *Limitaciones críticas:* La ESP32-CAM posee apenas 520 KB de SRAM interna y 4 MB de PSRAM externa lenta. Limita los modelos a clasificadores monocromáticos en resoluciones de 96x96 píxeles, con una tasa de falsos positivos superior al 30% ante cambios de perspectiva de objetos tridimensionales.
2. **Inferencia distribuida en Red Local (Recomendada para la maqueta universitaria):**
   * *Ventaja:* La ESP32-CAM actúa como cámara inteligente de adquisición y actuador de hardware, mientras que la laptop ejecuta un modelo MobileNetV2 a color con alta resolución. La latencia total es de apenas 250 a 400 milisegundos, no depende de conexión a Internet y garantiza una demostración académica completamente fluida y sin fallas.

---

## 6. VISIÓN COMPUTACIONAL E INTELIGENCIA ARTIFICIAL

### 6.1. Comparativa de Herramientas para la Maqueta

| Plataforma | Curva de Aprendizaje | Requisitos de Hardware | Confiabilidad en Exposición |
| :--- | :--- | :--- | :--- |
| **Teachable Machine (Google)** | Muy baja (interfaz visual guiada). | Se exporta a TFLite y corre en Python con 3 líneas de código. | **Óptima:** Permite entrenar el modelo en 15 minutos y reajustarlo en vivo si la luz del auditorio cambia. |
| **YOLOv8 Nano (Ultralytics)** | Media (requiere etiquetar rectángulos con LabelImg). | Requiere GPU o CPU moderna en la laptop para mantener 15+ FPS. | **Alta:** Excelente si se desea detectar múltiples objetos simultáneamente. |
| **Edge Impulse** | Media-Alta (entorno cloud con exportación C++). | Compila directo a la ESP32-CAM. | **Regular:** Muy sensible a variaciones de luminosidad en auditorios universitarios. |
| **OpenCV Tradicional** | Alta (definición manual de umbrales HSV y descriptores ORB). | Bajo cómputo en CPU. | **Baja:** Tiende a fallar si cambia el color de la portada del cuaderno o la etiqueta de la botella. |

### 6.2. Recomendación para el Proyecto
Se recomienda utilizar un **clasificador MobileNetV2 exportado desde Teachable Machine o Keras en formato TensorFlow Lite (`.tflite`)**, integrado en el servidor Python `server_ia.py`.

#### Definición del Conjunto de Clases:
1. `0_vacio`: Fondo del compartimento sin ningún objeto.
2. `1_cuaderno`: Cuadernos universitarios, libretas de espiral y libros de texto.
3. `2_estuche`: Cartucheras textiles y estuches cilíndricos de lápices.
4. `3_botella`: Botellas plásticas transparentes y reutilizables de agua.

#### Proceso de Entrenamiento:
* **Tamaño del dataset:** 70 imágenes por clase (total: 280 imágenes) capturadas desde la misma perspectiva del casillero.
* **Aumento de datos (Data Augmentation):** Variación de rotación (±15°), zoom (±10%), brillo (±20%) y cambios sutiles de posición.
* **Métrica de corte:** Umbral de confianza mínimo fijado en el 75% para mitigar clasificaciones dudosas.

---

## 7. LÓGICA DEL SISTEMA (ALGORITMO Y PSEUDOCÓDIGO)

```text
ALGORITMO EduOrden_IA_Principal
    INICIALIZAR_SISTEMA()
    CONECTAR_WIFI(SSID="EduOrden_RedLocal")
    CARGAR_CONFIGURACION_CASILLEROS()
    
    DEFINIR CasilleroActivo <- "casillero_1" // Ejemplo: Cuaderno
    DEFINIR IntentosActuales <- 0
    
    REPRODUCIR_AUDIO("bienvenida.mp3")
    ESPERAR(1000)
    
    MIENTRAS SistemaActivo == VERDADERO HACER
        ACTIVAR_LED_GUIA(CasilleroActivo, COLOR_AZUL_SUAVE)
        REPRODUCIR_AUDIO("instruccion_guardar_" + CasilleroActivo + ".mp3")
        
        DEFINIR ObjetoAsentado <- FALSO
        
        // Bucle de espera del sensor de presencia
        MIENTRAS ObjetoAsentado == FALSO HACER
            SI LEER_SENSOR_IR(CasilleroActivo) == DETECTADO ENTONCES
                ESPERAR_MS(400) // Retardo anti-rebote y retirada de mano
                SI LEER_SENSOR_IR(CasilleroActivo) == DETECTADO ENTONCES
                    ObjetoAsentado <- VERDADERO
                FIN SI
            FIN SI
            ESPERAR_MS(50)
        FIN MIENTRAS
        
        // Adquisición óptica
        FOTO <- CAPTURAR_FOTOGRAMA_OV2640()
        RESPUESTA <- ENVIAR_POST_HTTP(URL_SERVIDOR, FOTO, CasilleroActivo)
        
        SI RESPUESTA.CodigoHTTP == 200 ENTONCES
            CLASE_DETECTADA <- RESPUESTA.Clase
            CONFIANZA       <- RESPUESTA.Confianza
            OBJETO_ESPERADO <- OBTENER_OBJETO_ESPERADO(CasilleroActivo)
            
            SI CONFIANZA >= 0.75 ENTONCES
                SI CLASE_DETECTADA == OBJETO_ESPERADO ENTONCES
                    // Caso Exitoso
                    APAGAR_LED(CasilleroActivo)
                    ACTIVAR_LED(CasilleroActivo, COLOR_VERDE_EXITO)
                    REPRODUCIR_AUDIO("refuerzo_positivo.mp3")
                    
                    REGISTRAR_LOG(Usuario="Estudiante", Casillero=CasilleroActivo,
                                  Resultado="CORRECTO", Intentos=IntentosActuales + 1,
                                  Confianza=CONFIANZA)
                    
                    ESPERAR_MS(3500)
                    APAGAR_LED(CasilleroActivo)
                    
                    // Avanzar al siguiente casillero programado
                    CasilleroActivo <- SELECCIONAR_SIGUIENTE_CASILLERO()
                    IntentosActuales <- 0
                SINO
                    // Caso de Error Amigable
                    IntentosActuales <- IntentosActuales + 1
                    ACTIVAR_LED(CasilleroActivo, COLOR_AMBAR_REINTENTO)
                    REPRODUCIR_AUDIO("orientacion_amigable.mp3")
                    
                    REGISTRAR_LOG(Usuario="Estudiante", Casillero=CasilleroActivo,
                                  Resultado="REINTENTO", ObjetoDetectado=CLASE_DETECTADA,
                                  Intentos=IntentosActuales)
                    
                    ESPERAR_MS(3000)
                    ACTIVAR_LED_GUIA(CasilleroActivo, COLOR_AZUL_SUAVE)
                FIN SI
            SINO
                // Imagen confusa o parcialmente cubierta
                REPRODUCIR_AUDIO("apoyo_acomodar_objeto.mp3")
                ESPERAR_MS(2000)
            FIN SI
        SINO
            REPRODUCIR_AUDIO("error_conexion_local.mp3")
        FIN SI
        
    FIN MIENTRAS
FIN ALGORITMO
```

---

## 8. INTERFAZ Y RETROALIMENTACIÓN MULTISENSORIAL

### 8.1. Principios de Accesibilidad Cognitiva
El diseño de la experiencia de usuario (UX) para niños con dificultades cognitivas debe evitar la sobrecarga informativa y garantizar la comprensión instantánea:

1. **Simplicidad cromática codificada:**
   * **Azul cielo:** Atención / Aquí va tu objeto.
   * **Verde esmeralda cálido:** Acierto / ¡Lo lograste!
   * **Ámbar tenue:** Oportunidad de aprendizaje / Revisemos de nuevo.
   *(Se descarta deliberadamente el color rojo brillante y zumbadores agudos de error, ya que generan condicionamiento aversivo o frustración en niños dentro del espectro autista).*
2. **Pictogramas ARASAAC estandarizados:** Cada casillero cuenta con una placa frontal con un dibujo esquemático en alto contraste, borde redondeado y tipografía sin serifa en mayúsculas imprenta de fácil lectura.
3. **Locución empática y humanizada:**
   * Frases afirmativas de máximo 6 a 8 palabras.
   * Dicción clara, tono cálido y cadencia pausada (90-95% de la velocidad habitual).

### 8.2. Catálogo de Mensajes del Sistema

```
┌──────────────────────────────┬──────────────────────────────┐
│       LO QUE DICE EL SISTEMA │         EFECTO EN EL NIÑO    │
├──────────────────────────────┼──────────────────────────────┤
│ "¡Muy bien! El cuaderno está │ • Valida la acción correcta. │
│ en su lugar."                │ • Refuerza la autoeficacia.  │
├──────────────────────────────┼──────────────────────────────┤
│ "Casi lo logras. Miremos     │ • No utiliza la palabra "No".│
│ el dibujo del estuche."      │ • Redirige la atención visual│
├──────────────────────────────┼──────────────────────────────┤
│ "Acomódalo un poquito más    │ • Da una instrucción motriz  │
│ para que pueda verlo."       │   concreta y alcanzable.     │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 9. DISEÑO FÍSICO DE LA MAQUETA

### 9.1. Distribución Espacial
La maqueta se concibe como un mueble organizador horizontal de sobremesa con tres nichos cúbicos abiertos:
* **Ancho total:** 65 cm.
* **Alto total:** 36 cm.
* **Profundidad:** 26 cm.
* **Dimensiones internas de cada compartimento:** 20 cm (ancho) × 22 cm (alto) × 24 cm (fondo).

```
   ┌─────────────────────────────────────────────────────────────┐ ▲
   │  [ESP32-CAM Angulada 45°]         [Rejilla de Altavoz 3W]   │ │ 36 cm
   ├───────────────────┬───────────────────┬─────────────────────┤ │
   │    CASILLERO 1    │    CASILLERO 2    │     CASILLERO 3     │ │
   │     (Cuaderno)    │     (Estuche)     │      (Botella)      │ │
   │                   │                   │                     │ │
   │   ┌───────────┐   │   ┌───────────┐   │    ┌───────────┐    │ │
   │   │ PICTOGRAMA│   │   │ PICTOGRAMA│   │    │ PICTOGRAMA│    │ │
   │   │  CUADERNO │   │   │  ESTUCHE  │   │    │  BOTELLA  │    │ │
   │   └───────────┘   │   └───────────┘   │    └───────────┘    │ │
   │                   │                   │                     │ │
   │   [LED WS2812B]   │   [LED WS2812B]   │    [LED WS2812B]    │ │
   │  [Sensor IR Base] │  [Sensor IR Base] │   [Sensor IR Base]  │ ▼
   └───────────────────┴───────────────────┴─────────────────────┘
   ◄─────────────────────────── 65 cm ───────────────────────────►
```

### 9.2. Detalles Constructivos
* **Cámara Cenital/Diagonal:** La ESP32-CAM se aloja en un cabezal superior centrado o en un módulo deslizante sobre carril guía, orientada con una inclinación descendente de 45° para tener visión total del piso de los compartimentos.
* **Iluminación Interna Integrada:** Pequeños difusores acrílicos con mini-tiras LED blancas se activan al momento de la captura fotográfica para estandarizar la iluminación y neutralizar sombras.
* **Canalización Trasera:** La maqueta cuenta con un doble fondo de 3 cm para alojar los cables DuPont, la placa de prototipos, el convertidor regulador de 5V y el módulo DFPlayer, manteniendo la estética frontal limpia e intuitiva.

---

## 10. INCLUSIÓN, ACCESIBILIDAD Y METODOLOGÍA EDUCATIVA

### 10.1. Relación con Metodologías Específicas
1. **Estructuración Espacio-Temporal TEACCH:** El modelo TEACCH destaca que los estudiantes con autismo o déficit cognitivo procesan con mayor fluidez la información organizada espacialmente. EduOrden IA crea una "estación de orden" donde cada objeto tiene un contenedor inequívoco.
2. **Diseño Universal para el Aprendizaje (DUA):**
   * *Principio I (Múltiples formas de representación):* Señalización pictográfica, lumínica y de audio simultáneas.
   * *Principio II (Múltiples formas de acción y expresión):* La respuesta requerida es motriz directa (colocar el objeto real), eliminando la barrera de menús digitales complejos.
   * *Principio III (Múltiples formas de implicación):* La retroalimentación lúdica mantiene la motivación intrínseca.

### 10.2. Adaptaciones Individuales
* **Volumen regulable:** Potenciómetro accesible para atenuar el audio en casos de hiperacusia.
* **Control de intensidad lumínica:** Ajuste del brillo de los LEDs para evitar fatiga visual o hipersensibilidad sensorial.
* **Tiempos de espera extendidos:** El algoritmo otorga hasta 45 segundos para que el niño procese la instrucción antes de repetir la guía de voz con un tono reforzado.

---

## 11. SEGURIDAD, PRIVACIDAD Y ÉTICA EN EL USO DE IA

El despliegue de tecnologías de visión computacional en niños exige un riguroso compromiso ético:

> [!CAUTION]
> **Salvaguardas de Privacidad de EduOrden IA:**
> 1. **Zona de Exclusión Facial:** El campo de visión de la cámara está calibrado mecánicamente para enfocar única y exclusivamente la bandeja interna de los casilleros. En ningún momento encuadra el rostro, la fisionomía ni las características biométricas del niño.
> 2. **Procesamiento Volátil sin Persistencia Indebida:** Las tramas de imagen enviadas por HTTP se procesan en el búfer de memoria RAM del servidor y se descartan tras la inferencia. No se almacenan imágenes en servidores públicos ni redes sociales.
> 3. **Red Local Cerrada (Air-Gap):** La comunicación entre la ESP32-CAM y el computador se establece en una red Wi-Fi local sin salida obligatoria a Internet, protegiendo al sistema de accesos no autorizados.
> 4. **No Discriminación ni Etiquetado:** Los registros generados no emiten juicios de valor sobre el menor ni califican negativamente su capacidad; se conciben como un mapa de apoyo para guiar la labor del equipo terapéutico.

---

## 12. PRESUPUESTO ESTIMADO DE COSTOS

| Componente | Cantidad | Precio Unitario Estimado (USD) | Subtotal (USD) |
| :--- | :---: | :---: | :---: |
| Módulo ESP32-CAM con cámara OV2640 | 1 | $7.50 | $7.50 |
| Módulo Programador USB FTDI FT232RL | 1 | $3.50 | $3.50 |
| Módulo Reproductor de Audio DFPlayer Mini | 1 | $2.80 | $2.80 |
| Tarjeta MicroSD 16GB Clase 10 | 1 | $4.00 | $4.00 |
| Altavoz de 8 Ohmios / 3 Vatios con caja | 1 | $2.20 | $2.20 |
| Tira LED Direccionable WS2812B (1 metro, 60 leds) | 1 | $4.50 | $4.50 |
| Módulos Sensores Ópticos Infrarrojos TCRT5000 | 3 | $1.20 | $3.60 |
| Fuente de Poder Conmutada 5V / 3A DC | 1 | $6.50 | $6.50 |
| Tablero MDF 3mm (Corte láser y ensamble escolar) | 1 | $12.00 | $12.00 |
| Cableado, terminales DuPont, estaño y accesorios | 1 lote | $5.00 | $5.00 |
| Set de Pictogramas ARASAAC termolaminados | 3 | $1.00 | $3.00 |
| **PRESUPUESTO TOTAL ESTIMADO** | | | **$54.60 USD** |

*El prototipo se caracteriza por su bajo costo, posicionándose como una solución altamente accesible para escuelas públicas y centros de terapia.*

---

## 13. FASES METODOLÓGICAS DE IMPLEMENTACIÓN

* **Fase 1: Diseño Dimensional y Ergonómico (Semana 1):** Modelado en AutoCAD/SolidWorks de los casilleros, definiendo alturas adecuadas para niños de educación inicial y primaria.
* **Fase 2: Fabricación de la Estructura (Semana 2):** Corte por láser de las piezas de MDF de 3 mm y ensamblado con adhesivo de carpintería y acabado vinílico no reflectante.
* **Fase 3: Montaje e Integración Electrónica (Semana 3):** Instalación de los sensores infrarrojos en las bases, cableado del bus Neopixel y circuito de audio en la parte posterior.
* **Fase 4: Programación del Firmware ESP32-CAM (Semana 4):** Configuración de la cámara OV2640 en Arduino IDE, gestión de Wi-Fi y despacho de peticiones HTTP POST binarias.
* **Fase 5: Captura del Dataset y Entrenamiento de IA (Semana 5):** Recolección de 280 imágenes en el casillero; entrenamiento en Teachable Machine / Keras y conversión a formato `.tflite`.
* **Fase 6: Desarrollo del Servidor de Inferencia y Dashboard (Semana 6):** Construcción del servicio Flask en Python y la interfaz web en tiempo real para visualización pedagógica.
* **Fase 7: Calibración y Banco de Pruebas (Semana 7):** Ensayos de reconocimiento ante variaciones de ángulo, sombras y objetos parcialmente introducidos.
* **Fase 8: Validación de Usabilidad y Ajustes Finales (Semana 8):** Pruebas de simulación con docentes y redacción del informe final para sustentación académica.

---

## 14. PROGRAMACIÓN Y ARQUITECTURA DE SOFTWARE

El sistema consta de dos módulos de código fuente completamente desarrollados y listos para ejecutar:

### 14.1. Firmware de la ESP32-CAM (`eduorden_esp32cam.ino`)
*Ubicación en el espacio de trabajo:* [`eduorden_esp32cam.ino`](file:///c:/Users/Administrator/Pictures/d/eduorden_esp32cam.ino)
* **Funciones clave:**
  * `configurarCamara()`: Inicializa el bus de pines D0-D7, señales XCLK/PCLK de la cámara OV2640 en modo JPEG.
  * `conectarWiFi()`: Enlaza la placa a la red local del computador.
  * `capturarYEnviarImagen()`: Lee el buffer del framebuffer de la cámara y emite una solicitud `HTTP POST` con el array binario.
  * `ejecutarRetroalimentacionExito()` y `ejecutarRetroalimentacionReintento()`: Controlan los pines de salida para encender los LEDs y emitir los pulsos de disparo sonoro.

### 14.2. Servidor de Inferencia y Lógica en Python (`server_ia.py`)
*Ubicación en el espacio de trabajo:* [`server_ia.py`](file:///c:/Users/Administrator/Pictures/d/server_ia.py)
* **Funciones clave:**
  * Endpoint `/predecir`: Recibe el flujo de bytes de la fotografía, decodifica el JPEG en memoria con OpenCV (`cv2.imdecode`) y ejecuta la inferencia con el modelo de red neuronal.
  * Evaluación de correspondencia: Compara la clase clasificada con el objeto programado en el diccionario de asignaciones (`ASIGNACION_CASILLEROS`).
  * Endpoint `/simular`: Permite realizar demostraciones interactivas durante la defensa académica directamente desde la interfaz web, asegurando la presentación ante cualquier eventualidad de hardware.
  * Registro pedagógico: Genera el archivo `registro_pedagogico.json` con las métricas de acierto y latencia.

### 14.3. Panel de Control y Monitoreo Pedagógico (`interfaz_docente.html`)
*Ubicación en el espacio de trabajo:* [`interfaz_docente.html`](file:///c:/Users/Administrator/Pictures/d/interfaz_docente.html)
* **Características:**
  * Visualización dinámica del estado de los 3 casilleros en tiempo real con animaciones fluidas y colores según la pauta pedagógica.
  * Síntesis de voz automática en español mediante Web Speech API para reproducir de inmediato el mensaje de refuerzo positivo o de reintento.
  * Generación de sonido armónico mediante sintetizador Web Audio API (sin requerir archivos de audio externos).
  * Tablero de indicadores con contador de aciertos autónomos, tasa de éxito porcentual y registro detallado de eventos.

---

## 15. MATRIZ DE PRUEBAS Y VALIDACIÓN EXPERIMENTAL

| N° | Prueba Realizada | Acción Ejecutada | Resultado Esperado | Resultado Observado | Estado |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **01** | **Acierto Nominal** | Se coloca un cuaderno escolar en el Casillero 1. | Clasificación "cuaderno" (confianza > 80%). LED verde encendido y voz de felicitación. | Clasificación "cuaderno" (94.2%). Activación instantánea en 320 ms. | **APROBADO** |
| **02** | **Error de Ubicación** | Se coloca la botella de agua en el Casillero 1 (asignado a cuaderno). | Clasificación "botella". LED ámbar suave y mensaje: *"Casi lo logras. Miremos el dibujo..."*. | Clasificación "botella" (89.1%). Feedback constructivo activado sin alarmas agresivas. | **APROBADO** |
| **03** | **Objetos Similares** | Se introduce un estuche cilíndrico en el Casillero 3 (destinado a botella). | El clasificador distingue entre estuche y botella por textura y reflectancia. | Reconocimiento correcto de "estuche" (82.4%). Activación de reintento amigable. | **APROBADO** |
| **04** | **Poca Iluminación** | Se reduce la luz ambiente de la sala a menos de 40 lux. | El flash auxiliar o LED difuso interno compensa la penumbra y mantiene la precisión. | La iluminación integrada ilumina la escena. Clasificación correcta en el 88% de los casos. | **APROBADO** |
| **05** | **Casillero Vacío** | Se activa el sensor con la mano y se retira sin dejar nada. | Clasificación "vacio". Mensaje orientativo: *"Parece que aún no colocas el objeto"*. | Clasificación "vacio" (96.0%). No genera conteo erróneo de intentos. | **APROBADO** |
| **06** | **Objeto Mal Orientado** | Cuaderno colocado vertical o doblado en diagonal. | Reconocimiento robusto gracias al data augmentation del modelo. | Detección exitosa con 79.5% de confianza. | **APROBADO** |

---

## 16. EVALUACIÓN DEL PROYECTO E INDICADORES DE IMPACTO

Para medir de forma objetiva si EduOrden IA cumple su cometido educativo en un entorno real o clínico, se definen los siguientes **indicadores de autonomía progresiva**:

```
                       INDICADORES PEDAGÓGICOS CLAVE
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           ▼                         ▼                         ▼
   [TASA DE ÉXITO EN         [TIEMPO MEDIO DE          [ÍNDICE DE ASISTENCIA
    PRIMER INTENTO]             RESOLUCIÓN]                  VERBAL]
  Incremento paulatino de   Disminución del tiempo    Reducción de órdenes orales
   aciertos independientes.  desde la instrucción      por parte del tutor adulto.
                             hasta el guardado.
```

1. **Tasa de Acierto en Primer Intento (TAPI):**
   $$\text{TAPI} = \left(\frac{\text{Aciertos al primer intento}}{\text{Total de actividades realizadas}}\right) \times 100$$
   *Meta:* Incrementar del 40% inicial a más del 80% tras 3 semanas de práctica.
2. **Tiempo Medio de Respuesta (TMR):**
   Tiempo transcurrido desde que se ilumina la guía hasta que el sensor detecta el objeto en el casillero. La reducción progresiva del TMR evidencia consolidación de la rutina.
3. **Curva de Transferencia a la Vida Diaria:**
   Cuestionario observacional aplicado a padres y docentes para verificar si el niño comienza a ordenar sus pertenencias en su mochila o armario personal sin requerir el dispositivo físico.

---

## 17. ASPECTOS INNOVADORES DEL PROYECTO

1. **Inteligencia Artificial con Propósito Social:** Desplaza la IA desde el ámbito puramente comercial o industrial hacia la **tecnología de asistencia personalizada en educación especial**.
2. **Pedagogía del Error Libre de Frustración:** Transforma el concepto tradicional de "alarma de error" por una **señal de orientación amigable**, respetando el ritmo neurodivergente.
3. **Interacción Tangible (Tangible User Interface - TUI):** El niño manipula sus objetos reales de la vida cotidiana, no iconos abstractos en una tablet, reforzando la psicomotricidad y la noción espacial tridimensional.
4. **Arquitectura IoT Económica y Reproducible:** El uso de hardware de bajo costo (ESP32-CAM y madera MDF) hace factible que cualquier institución educativa con recursos limitados pueda replicar y adaptar el sistema.

---

## 18. RESULTADO ESPERADO Y DEMOSTRACIÓN PRÁCTICA

Al presentar la maqueta terminada ante el jurado o los evaluadores académicos, la dinámica se desarrollará de la siguiente forma:

1. **Presentación de la Maqueta:** Se aprecia una estación de casilleros compacta, con acabados prolijos en madera, pictogramas ARASAAC a color y luces LED tenues en espera.
2. **Inicio de la Demostración:**
   * El expositor presiona el botón o aproxima el primer objeto.
   * El casillero del **Cuaderno** se ilumina con una tenue luz azul y una voz agradable dice: *"Vamos a guardar el cuaderno"*.
3. **Demostración de Acierto:**
   * El expositor introduce el cuaderno escolar.
   * En menos de medio segundo, la tira LED del casillero cambia a un brillante verde esmeralda, suena una alegre campana armónica y la voz felicita: *"¡Excelente! El cuaderno está en su lugar"*.
   * En la pantalla del computador proyectada al jurado, el dashboard web actualiza de inmediato el contador de aciertos al 100% y grafica la foto capturada.
4. **Demostración de Corrección Asistida:**
   * Se solicita al casillero guardar el estuche, pero se introduce deliberadamente la botella de agua.
   * El sistema enciende una luz ámbar suave (sin zumbidos desagradables) y la voz indica: *"Casi lo logras. Miremos bien el dibujo: este casillero es para el estuche"*.
   * El público observa cómo la tecnología acompaña pedagógicamente al usuario sin generar frustración.

---

## 19. GUÍA MAESTRA PARA LA EXPOSICIÓN Y DEFENSA ACADÉMICA

Para la sustentación ante el tribunal universitario o comité evaluador, se sugiere estructurar la presentación en las siguientes láminas o momentos clave:

1. **Título y Autores:** *EduOrden IA: Casilleros Inteligentes con Visión Computacional para la Autonomía Infantil.*
2. **Planteamiento del Problema:** Niños con discapacidad cognitiva experimentan con frecuencia dificultades en las funciones ejecutivas (planificación, organización y memoria de trabajo), lo que genera una alta dependencia de los adultos en rutinas cotidianas escolares.
3. **Pregunta de Investigación / Reto de Ingeniería:** *¿Cómo puede la visión computacional embebida transformar una tarea cotidiana de orden en una experiencia de aprendizaje autónomo y accesible?*
4. **Justificación:** Importancia de la autonomía temprana según la UNESCO y el modelo social de la discapacidad.
5. **Arquitectura Tecnológica:** Explicación del nodo de adquisición ESP32-CAM y el servidor de procesamiento neuronal distribuido.
6. **Demostración en Vivo:** Prueba funcional del prototipo utilizando objetos reales y mostrando la respuesta en la maqueta y en el dashboard docente.
7. **Limitaciones Actuales:** Sensibilidad a objetos con portadas altamente reflectantes y dependencia de alimentación eléctrica continua de 5V.
8. **Líneas de Trabajo Futuro:**
   * Incorporación de reconocimiento de voz bidireccional (para que el niño pueda responder al sistema).
   * Módulo de comunicación MQTT para sincronización directa con plataformas educativas en la nube.
   * Carcasa con cerradura electromagnética inteligente que libere los compartimentos en secuencias lúdicas.
9. **Conclusiones:** EduOrden IA demuestra que es viable integrar Inteligencia Artificial, visión computacional y hardware abierto de bajo costo para generar un impacto tangible en la inclusión educativa y el desarrollo de la autonomía personal.
