# 🎒 EduOrden IA
> **Casilleros Inteligentes con ESP32-CAM y Visión Computacional para el Fomento de la Autonomía en Niños con Discapacidad Cognitiva**

---

## 📌 Descripción General
**EduOrden IA** es un proyecto tecnológico-educativo universitario diseñado para asistir y motivar a niños con discapacidad cognitiva (como síndrome de Down, TEA o dificultades en funciones ejecutivas) en sus actividades diarias de organización y reconocimiento de objetos escolares.

El sistema utiliza una **ESP32-CAM** para capturar imágenes del interior de compartimentos inteligentes y un servidor local con **Inteligencia Artificial (TensorFlow Lite / OpenCV)** para verificar si el objeto depositado (cuaderno, estuche de lápices, botella de agua) corresponde al casillero asignado.

El sistema proporciona **retroalimentación multisensorial positiva e inmediata**:
* **Acierto:** Luz LED verde esmeralda, melodía armónica y refuerzo verbal empático.
* **Reintento Asistido:** Luz ámbar suave (sin zumbidos molestos ni alarmas punitivas) e indicación amigable para volver a intentar.

---

## 📂 Estructura del Repositorio

```text
EDUORDEN-IA/
│
├── DOCUMENTO_TECNICO_EDUORDEN_IA.md   # Documento académico completo con las 19 secciones detalladas
├── eduorden_esp32cam.ino              # Firmware en C++ para la placa ESP32-CAM (Arduino IDE)
├── server_ia.py                       # Servidor de inferencia en Python con Flask y visión computacional
├── interfaz_docente.html              # Dashboard pedagógico en tiempo real con síntesis de voz y métricas
├── entrenar_dataset.py                # Script auxiliar para captura de dataset y entrenamiento
├── .gitignore                         # Archivos ignorados por control de versiones
└── README.md                          # Este archivo de presentación
```

---

## 🚀 Puesta en Marcha Rápida

### 1. Panel de Control y Simulación (Sin necesidad de hardware)
Abre el archivo `interfaz_docente.html` directamente en tu navegador web (Google Chrome, Edge, etc.) para interactuar con los casilleros, escuchar los mensajes hablados en español y simular aciertos y reintentos.

### 2. Servidor de Inteligencia Artificial (Python)
Instala las dependencias necesarias:
```bash
pip install flask flask-cors opencv-python numpy
```

Ejecuta el servidor:
```bash
python server_ia.py
```
El servidor escuchará en el puerto `5000` en el endpoint `POST /predecir`.

### 3. Firmware de la ESP32-CAM (Arduino IDE)
1. Abre `eduorden_esp32cam.ino` en el Arduino IDE.
2. Selecciona la placa **"AI Thinker ESP32-CAM"**.
3. Configura las credenciales de tu red Wi-Fi local:
   ```cpp
   const char* WIFI_SSID     = "TuRedWiFi";
   const char* WIFI_PASSWORD = "TuClaveWiFi";
   const char* SERVER_URL    = "http://<IP_DE_TU_PC>:5000/predecir";
   ```
4. Carga el código utilizando un módulo FTDI USB-TTL.

---

## 💡 Innovación y Metodología Pedagógica
* **Estructuración Espacio-Temporal TEACCH:** Espacios claros con pictogramas ARASAAC estandarizados.
* **Diseño Universal para el Aprendizaje (DUA):** Múltiples formas de representación sensorial (visual, auditiva y táctil).
* **Privacidad Infantil Garantizada:** La cámara está angulada exclusivamente al fondo del casillero; nunca enfoca rostros ni almacena datos personales en la nube.

---

## 👥 Autores
Proyecto desarrollado para presentación y defensa académica universitaria.
