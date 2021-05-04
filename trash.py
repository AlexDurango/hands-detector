# from google.protobuf.json_format import MessageToDict
import turtle 
import cv2
import mediapipe as mp
import math

wcam = cv2.VideoCapture(1)

##### Window Settings #####

wn = turtle.Screen()
wn.title("i hate turtles")
wn.bgcolor("#888888")
wn.setup(width=640, height=480)

#########################

###### Configuración del lapiz #####

defaultPenSize = 3

pen = turtle.Turtle()
pen.shape("circle")
pen.color("red")
pen.pensize(defaultPenSize)

# eraser = turtle.Turtle()
# eraser.shape("circle")
# eraser.color("#080808")
# eraser.width(20)
# eraser.pensize(20)

##############################

#-------------- CV2 y Hand Traking ------------ #
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:

  while wcam.isOpened():

    success, image = wcam.read()

    if not success:
      print("No se encontró la cámara.")
      continue

    # Obtiene las dimensiones de la cámara
    heightCam, widthCam = image.shape[0], image.shape[1]

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

    #############################################3

    # Si encuentra puntos de la mano:
    if results.multi_hand_landmarks:

      # handedness_dict = {}

      # for idx, hand_handedness in enumerate(results.multi_handedness):
      #   handedness_dict = MessageToDict(hand_handedness)
      #   # print(handedness_dict['classification'][0]['label'])  # Saber si la mano es derecha o izquierda


      for hand_landmarks in results.multi_hand_landmarks:

        # Dibuja las marcas de las manos detectadas en la imagen a mostrar
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # OBTENER LAS CORDENADAS DE LOS DEDOS
        coordThumbX = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * widthCam) 
        coordThumbY = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * heightCam)
        coordIndexX = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * widthCam) 
        coordIndexY = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * heightCam)

        image = cv2.circle(image, (coordThumbX, coordThumbY), 10, (0,0,255), -1)
        image = cv2.circle(image, (coordIndexX, coordIndexY), 10, (255,0,0), -1)

        # Distance entre index y pulgar

        # if handedness_dict['classification'][0]['label'] == "Right":

        #   pen.showturtle()

        #   eraser.penup()
        #   eraser.hideturtle()

        distanceIndexThumb = math.sqrt(((coordThumbX-coordIndexX)**2)+ ((coordThumbY-coordIndexY)**2))

        # -------------  Dibujo del lapiz ------------- #
        if distanceIndexThumb < 40:
          pen.penup()
        else:
          pen.pendown()
        turtleCoordX, turtleCoordY = coordIndexX-320, 240 - coordIndexY 
        pen.goto(turtleCoordX, turtleCoordY)
        # --------------------------------------------- #
        
        # if  handedness_dict['classification'][0]['label'] == "Left":
        #   eraser.showturtle()

        #   pen.penup()
        #   pen.hideturtle()

        #   distanceIndexThumb = math.sqrt(((coordThumbX-coordIndexX)**2)+ ((coordThumbY-coordIndexY)**2))

        #   if distanceIndexThumb < 40:
        #     eraser.penup()
        #   else:
        #     eraser.pendown()

        #   turtleCoordX, turtleCoordY = coordIndexX-320, 240 - coordIndexY 
        #   eraser.goto(turtleCoordX, turtleCoordY)

    # Muestra la imagen con las marcas de la mano
    cv2.imshow('sample texttttttttt', image)

    if cv2.waitKey(2) & 0xFF == ord('c'):
      pen.clear()

    if cv2.waitKey(1) & 0xFF == ord('g'):
      pen.color("green")

    if cv2.waitKey(1) & 0xFF == ord('b'):
      pen.color("blue")
    
    if cv2.waitKey(1) & 0xFF == ord('r'):
      pen.color("red")

    if cv2.waitKey(1) & 0xFF == ord('+'):
      defaultPenSize = defaultPenSize + 1
      pen.pensize(defaultPenSize)

    if cv2.waitKey(1) & 0xFF == ord('-'):
      defaultPenSize = defaultPenSize - 1
      pen.pensize(defaultPenSize)

    if cv2.waitKey(1) & 0xFF == ord('x'):
      for i in range(30):
        pen.undo()

    # Espera hasta que se presione la tecla ESC
    if cv2.waitKey(5) & 0xFF == 27:
      pen.screen.bye()
      break


wcam.release()