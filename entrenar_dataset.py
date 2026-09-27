"""
======================================================================================
PROYECTO: EduOrden IA - Asistente de Recolección de Dataset y Entrenamiento
DESCRIPCIÓN:
    Script de apoyo para capturar muestras de entrenamiento desde la ESP32-CAM
    o cámara web USB, organizar carpetas por clase y exportar a TensorFlow Lite.
======================================================================================
"""

import os
import cv2
import time

CLASES = ["vacio", "cuaderno", "estuche", "botella", "lonchera"]
DATASET_DIR = "dataset_entrenamiento"

def crear_estructura_carpetas():
    for clase in CLASES:
        ruta = os.path.join(DATASET_DIR, clase)
        os.makedirs(ruta, exist_ok=True)
    print(f"[OK] Carpetas creadas en '{DATASET_DIR}/' para las clases: {CLASES}")

def capturar_desde_camara_web(clase_seleccionada, num_fotos=50):
    """Permite tomar fotos con la webcam de la laptop colocándola frente a la maqueta."""
    ruta_clase = os.path.join(DATASET_DIR, clase_seleccionada)
    os.makedirs(ruta_clase, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] No se pudo acceder a la cámara web.")
        return

    print(f"\n--- Iniciando captura para: {clase_seleccionada.upper()} ---")
    print("Presiona ESPACIO para capturar una foto | Presiona 'Q' para salir.")

    conteo = 0
    while conteo < num_fotos:
        ret, frame = cap.read()
        if not ret:
            break

        # Mostrar visor con guías
        h, w, _ = frame.shape
        cv2.rectangle(frame, (int(w*0.2), int(h*0.15)), (int(w*0.8), int(h*0.85)), (0, 255, 0), 2)
        cv2.putText(frame, f"Clase: {clase_seleccionada} | Fotos: {conteo}/{num_fotos}", 
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Espacio: Guardar | Q: Finalizar", 
                    (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Captura de Dataset - EduOrden IA", frame)
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord(' '):
            nombre_archivo = os.path.join(ruta_clase, f"{clase_seleccionada}_{int(time.time()*1000)}.jpg")
            # Guardar el recorte central para mejorar la invarianza
            recorte = frame[int(h*0.15):int(h*0.85), int(w*0.2):int(w*0.8)]
            cv2.imwrite(nombre_archivo, recorte)
            conteo += 1
            print(f"[{conteo}/{num_fotos}] Guardada: {nombre_archivo}")
        elif tecla == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[Completado] Se guardaron {conteo} imágenes para '{clase_seleccionada}'.")

if __name__ == "__main__":
    crear_estructura_carpetas()
    print("""
    ==================================================
        GENERADOR DE DATASET - EDUORDEN IA
    ==================================================
    1. vacío (fondo del casillero sin objetos)
    2. cuaderno
    3. estuche
    4. botella
    5. lonchera
    ==================================================
    """)
    print("Para entrenar el modelo fácilmente:")
    print("1. Sube estas carpetas a https://teachablemachine.withgoogle.com/")
    print("2. Exporta el modelo como 'TensorFlow Lite (Float32 o Quantized)'")
    print("3. Coloca el archivo 'modelo_eduorden.tflite' en la misma carpeta que 'server_ia.py'.")
