import mediapipe as mp
import cv2

wcam = cv2.VideoCapture(1)

#-------------- CV2 y Hand Traking ------------ #
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:

  while wcam.isOpened():

    success, image = wcam.read()

    if not success:
      print("No se encontró la cámara.")
      continue
    
    ############ Cv2 configuration ###############3

    # Convierte los colores BGR a RGB y voltea la imagen
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    #Mejorar el rendimiento
    image.flags.writeable = False

    # Porcesa la imagen de la cámara y devuelve la posición de la mano
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    #Convierte la imagen de nuevo de RGB a BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #############################################

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            # Dibuja las marcas de las manos detectadas en la imagen a mostrar
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Muestra la imagen con las marcas de la mano
    cv2.imshow('roses are red, i want to die', image)

    # Espera hasta que se presione la tecla ESC
    if cv2.waitKey(5) & 0xFF == 27:
      break


wcam.release()