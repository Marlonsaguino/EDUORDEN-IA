"""
======================================================================================
PROYECTO: EduOrden IA - Servidor de Visión Computacional e Inteligencia Artificial
AUTOR: Equipo de Desarrollo EduOrden IA
DESCRIPCIÓN:
    Servidor local en Python (Flask) para inferencia de imágenes provenientes de
    la ESP32-CAM. Evalúa la correspondencia del objeto con el casillero asignado,
    genera retroalimentación estructurada y registra métricas pedagógicas.
======================================================================================
"""

import os
import time
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS
import numpy as np
import cv2

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)
CORS(app)

# ======================== CONFIGURACIÓN DEL SISTEMA ========================
# Diccionario de asignación de casilleros a objetos esperados
ASIGNACION_CASILLEROS = {
    "casillero_1": {"objeto_esperado": "cuaderno",  "nombre_amigable": "Cuaderno escolar", "color": "#4A90E2"},
    "casillero_2": {"objeto_esperado": "estuche",   "nombre_amigable": "Estuche de lápices", "color": "#F5A623"},
    "casillero_3": {"objeto_esperado": "botella",   "nombre_amigable": "Botella de agua",   "color": "#7ED321"}
}

# Clases reconocidas por el modelo
CLASES_MODELO = ["vacio", "cuaderno", "estuche", "botella", "lonchera"]

# Directorios de trabajo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURES_DIR = os.path.join(BASE_DIR, "capturas")
LOGS_FILE = os.path.join(BASE_DIR, "registro_pedagogico.json")
MODEL_PATH = os.path.join(BASE_DIR, "modelo_eduorden.tflite")

os.makedirs(CAPTURES_DIR, exist_ok=True)

# Variable global para el intérprete de TensorFlow Lite (si existe el archivo .tflite)
tflite_interpreter = None
input_details = None
output_details = None

try:
    # Intentar cargar TensorFlow Lite Runtime
    import tflite_runtime.interpreter as tflite
    if os.path.exists(MODEL_PATH):
        tflite_interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        tflite_interpreter.allocate_tensors()
        input_details = tflite_interpreter.get_input_details()
        output_details = tflite_interpreter.get_output_details()
        logging.info("Modelo TensorFlow Lite cargado exitosamente.")
    else:
        logging.warning("No se encontró 'modelo_eduorden.tflite'. Se utilizará el motor de inferencia heurístico/simulado para pruebas académicas.")
except Exception as e:
    logging.warning(f"TFLite no disponible directamente ({e}). Utilizando analizador de imagen OpenCV.")

# Buffer de eventos en tiempo real para actualización de la interfaz del profesor
ultimos_eventos = []

# ======================== FUNCIONES DE PROCESAMIENTO ========================
def preprocesar_imagen(imagen_cv2, target_size=(224, 224)):
    """Prepara el array de imagen para la red neuronal normalizando valores."""
    img_redim = cv2.resize(imagen_cv2, target_size)
    img_rgb = cv2.cvtColor(img_redim, cv2.COLOR_BGR2RGB)
    img_norm = (img_rgb.astype(np.float32) / 127.5) - 1.0  # Normalización [-1, 1] típica de MobileNet
    return np.expand_dims(img_norm, axis=0)

def inferir_objeto(imagen_cv2):
    """
    Realiza la clasificación del objeto.
    Si hay modelo .tflite, infiere con la red.
    En caso contrario, aplica análisis de características visuales con OpenCV
    para garantizar una demostración funcional sin dependencias pesadas.
    """
    global tflite_interpreter
    if tflite_interpreter is not None:
        tensor_in = preprocesar_imagen(imagen_cv2)
        tflite_interpreter.set_tensor(input_details[0]['index'], tensor_in)
        tflite_interpreter.invoke()
        prediccion = tflite_interpreter.get_tensor(output_details[0]['index'])[0]
        indice_max = int(np.argmax(prediccion))
        confianza = float(prediccion[indice_max])
        clase = CLASES_MODELO[indice_max] if indice_max < len(CLASES_MODELO) else "desconocido"
        return clase, confianza
    else:
        # Motor heurístico visual para demostración académica
        # Analiza histograma de color dominante y varianza de brillo en la escena
        hsv = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2HSV)
        brillo_medio = np.mean(hsv[:, :, 2])
        saturacion_media = np.mean(hsv[:, :, 1])
        
        # Detección de color predominante
        hue_medio = np.mean(hsv[:, :, 0])
        
        if brillo_medio < 35:
            return "vacio", 0.92
        elif 90 <= hue_medio <= 130: # Predominio azul/celeste -> Cuaderno
            return "cuaderno", 0.88
        elif 10 <= hue_medio <= 30 or 150 <= hue_medio <= 180: # Rojo/Naranja -> Estuche
            return "estuche", 0.85
        elif 35 <= hue_medio <= 85: # Verde / Traslúcido -> Botella
            return "botella", 0.89
        else:
            # Detección por proporción geométrica si hay contornos
            gray = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
            contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contornos:
                c = max(contornos, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                relacion_aspecto = float(h) / max(w, 1)
                if relacion_aspecto > 1.6:
                    return "botella", 0.84
                elif 1.1 <= relacion_aspecto <= 1.5:
                    return "cuaderno", 0.86
                else:
                    return "estuche", 0.82
            return "cuaderno", 0.80

def guardar_registro_pedagogico(evento):
    """Almacena el registro para seguimiento de autonomía y aprendizaje."""
    registros = []
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                registros = json.load(f)
        except Exception:
            registros = []
    
    registros.append(evento)
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

# ======================== ENDPOINTS DE LA API ========================
@app.route("/predecir", methods=["POST"])
def predecir():
    """
    Endpoint principal que recibe la imagen binaria JPEG desde la ESP32-CAM
    mediante HTTP POST directo.
    """
    inicio_tiempo = time.time()
    casillero_id = request.args.get("casillero", "casillero_1")
    info_casillero = ASIGNACION_CASILLEROS.get(casillero_id, {"objeto_esperado": "cuaderno", "nombre_amigable": "General"})

    datos_imagen = request.data
    if not datos_imagen:
        return jsonify({"error": "No se recibieron datos de imagen"}), 400

    # Decodificar imagen desde el buffer binario en memoria
    nparr = np.frombuffer(datos_imagen, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "No se pudo decodificar el formato JPEG"}), 400

    # Guardar captura con timestamp para respaldo de pruebas (opcional)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{casillero_id}_{timestamp_str}.jpg"
    ruta_guardado = os.path.join(CAPTURES_DIR, nombre_archivo)
    cv2.imwrite(ruta_guardado, img)

    # Inferencia de IA
    clase_detectada, confianza = inferir_objeto(img)
    tiempo_procesamiento_ms = round((time.time() - inicio_tiempo) * 1000, 2)

    # Evaluación pedagógica de correspondencia
    es_correcto = (clase_detectada == info_casillero["objeto_esperado"])
    resultado_texto = "CORRECTO" if es_correcto else "INCORRECTO"

    # Generación de mensajes constructivos y libres de frustración
    if es_correcto:
        mensaje_voz = f"¡Muy bien! El {info_casillero['nombre_amigable']} está en su lugar correcto."
        tipo_alerta = "exito"
    elif clase_detectada == "vacio":
        mensaje_voz = "Parece que aún no has colocado el objeto. ¡Inténtalo con calma!"
        tipo_alerta = "espera"
    else:
        mensaje_voz = f"Casi lo logras. Recuerda que en este casillero guardamos: {info_casillero['nombre_amigable']}."
        tipo_alerta = "reintento"

    # Estructura del evento pedagógico
    evento = {
        "timestamp": datetime.now().isoformat(),
        "casillero": casillero_id,
        "esperado": info_casillero["objeto_esperado"],
        "detectado": clase_detectada,
        "confianza": round(confianza * 100, 1),
        "resultado": resultado_texto,
        "mensaje": mensaje_voz,
        "tipo_alerta": tipo_alerta,
        "latencia_ms": tiempo_procesamiento_ms,
        "foto_url": f"/captura/{nombre_archivo}"
    }

    guardar_registro_pedagogico(evento)
    ultimos_eventos.insert(0, evento)
    if len(ultimos_eventos) > 50:
        ultimos_eventos.pop()

    logging.info(f"Casillero: {casillero_id} | Esperado: {info_casillero['objeto_esperado']} | Detectado: {clase_detectada} ({confianza*100:.1f}%) | Resultado: {resultado_texto}")

    return jsonify(evento), 200

@app.route("/simular", methods=["POST"])
def simular():
    """
    Permite probar el sistema desde la interfaz web sin tener la cámara física conectada.
    Ideal para presentaciones en vivo y pruebas previas.
    """
    data = request.json or {}
    casillero_id = data.get("casillero", "casillero_1")
    objeto_ingresado = data.get("objeto", "cuaderno")
    
    info_casillero = ASIGNACION_CASILLEROS.get(casillero_id, {"objeto_esperado": "cuaderno", "nombre_amigable": "General"})
    es_correcto = (objeto_ingresado == info_casillero["objeto_esperado"])
    
    if es_correcto:
        mensaje_voz = f"¡Excelente trabajo! Has guardado el {info_casillero['nombre_amigable']} en su casillero."
        tipo_alerta = "exito"
    else:
        mensaje_voz = f"Casi. Miremos juntos el pictograma de este casillero: corresponde a {info_casillero['nombre_amigable']}."
        tipo_alerta = "reintento"

    evento = {
        "timestamp": datetime.now().isoformat(),
        "casillero": casillero_id,
        "esperado": info_casillero["objeto_esperado"],
        "detectado": objeto_ingresado,
        "confianza": 96.5,
        "resultado": "CORRECTO" if es_correcto else "INCORRECTO",
        "mensaje": mensaje_voz,
        "tipo_alerta": tipo_alerta,
        "latencia_ms": 12.4,
        "foto_url": None
    }
    
    guardar_registro_pedagogico(evento)
    ultimos_eventos.insert(0, evento)
    return jsonify(evento), 200

@app.route("/eventos", methods=["GET"])
def obtener_eventos():
    """Devuelve los últimos eventos registrados para actualizar la interfaz web en vivo."""
    return jsonify({
        "eventos": ultimos_eventos,
        "casilleros": ASIGNACION_CASILLEROS
    })

@app.route("/metricas", methods=["GET"])
def obtener_metricas():
    """Calcula indicadores de logro de autonomía para el docente o terapeuta."""
    if not os.path.exists(LOGS_FILE):
        return jsonify({"total_intentos": 0, "tasa_acierto": 0, "aciertos": 0, "reintentos": 0})

    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        registros = json.load(f)

    if not registros:
        return jsonify({"total_intentos": 0, "tasa_acierto": 0, "aciertos": 0, "reintentos": 0})

    total = len(registros)
    aciertos = sum(1 for r in registros if r.get("resultado") == "CORRECTO")
    reintentos = total - aciertos
    tasa = round((aciertos / total) * 100, 1)

    return jsonify({
        "total_intentos": total,
        "aciertos": aciertos,
        "reintentos": reintentos,
        "tasa_acierto": tasa
    })

if __name__ == "__main__":
    print("""
    ============================================================
      SERVIDOR EDUORDEN IA ACTIVO Y ESCUCHANDO
      Puerto: 5000
      Endpoint para ESP32-CAM: http://<TU_IP_LOCAL>:5000/predecir
    ============================================================
    """)
    app.run(host="0.0.0.0", port=5000, debug=False)
