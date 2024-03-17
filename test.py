import cv2

# Crear un objeto VideoCapture. El argumento 0 indica que se debe usar la cámara web predeterminada.
cap = cv2.VideoCapture(0)

while True:
    # Capturar frame por frame
    ret, frame = cap.read()

    # Mostrar el frame resultante
    cv2.imshow('Webcam', frame)

    # Si se presiona la tecla 'q', se rompe el bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando todo está hecho, liberar la captura
cap.release()
cv2.destroyAllWindows()