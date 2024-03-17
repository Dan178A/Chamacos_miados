import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import threading
import pygame 
from math import acos, degrees
def find_available_camera():
    for i in range(2):  # Prueba con las cámaras 0 y 1
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"La cámara {i} está disponible.")
            cap.release()
            return i
    print("No se encontró ninguna cámara disponible.")
    return None
def xScale( value, width):
    return (value / 100) * width

def invertXScale( value, width):
    return (value / width) * 100

def yScale( value, height):
    return (value / 100) * height

def invertYScale( value, height):
    return (value / height) * 100

def palm_centroid(coordinates_list):
    coordinates = np.array(coordinates_list)
    centroid = np.mean(coordinates, axis=0)
    centroid = int(centroid[0]), int(centroid[1])
    return centroid
class camara:
    player = None
    def __init__(self,player_):
        global player
        player = player_
        pygame.init()

    def init(self, printHand=False, lengthCenterLine=1, lengthCirc=1):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands


        close_hand = cv2.imread('./images/close-hand.jpg')
        close_hand_resized = cv2.resize(close_hand, (100, 100))
        close_hand_resized = np.array(close_hand_resized, dtype=np.uint8)

        open_hand = cv2.imread('./images/open-hand.jpg')
        open_hand_resized = cv2.resize(open_hand, (100, 100))
        open_hand_resized = np.array(open_hand_resized, dtype=np.uint8)

        camera_index = find_available_camera()
        if camera_index is not None:
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        else:
            return

        # Pulgar
        thumb_points = [1, 2, 4]

        # Indice, medio, anular y meñique
        palm_points = [0, 1, 2, 5, 9, 13, 17]

        fingertips_points = [8, 12, 16, 20]
        finger_base_points = [6, 10, 14, 18]

        # Colores
        GREEN = (48, 255, 48)
        BLUE = (192, 101, 21)
        YELLOW = (128, 64, 128)
        PURPLE = (128, 64, 128)
        PEACH = (180, 229, 255)

        with mp_hands.Hands(
            model_complexity=1,
            # Establecer en False si se utiliza video y True si se usan imagenes
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            fingers_counter = "_"

            while True:
                thickness = [2, 2, 2, 2, 2]
                ret, frame = cap.read()
                if ret == False:
                    break

                frame = cv2.flip(frame, 1)
                height, width, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                radio = int(height/3)
                center = np.array([int(width/2), int(height/2)])
                cv2.circle(frame, (center[0], center[1]),
                           radio, (0, 255, 0), lengthCirc)

                cerrado = False

                if results.multi_hand_landmarks:
                    coordinates_thumb = []
                    coordinates_palm = []
                    coordinates_ft = []
                    coordinates_fb = []
                    for hand_landmarks in results.multi_hand_landmarks:

                        # Obtener puntos de la palma de la mano
                        for index in palm_points:
                            x = int(hand_landmarks.landmark[index].x * width)
                            y = int(hand_landmarks.landmark[index].y * height)
                            coordinates_palm.append([x, y])
                        # Obtener puntos de la punta de los dedos
                        for index in fingertips_points:
                            x = int(hand_landmarks.landmark[index].x * width)
                            y = int(hand_landmarks.landmark[index].y * height)
                            coordinates_ft.append([x, y])
                        # Obtener puntos de la base de los dedos
                        for index in finger_base_points:
                            x = int(hand_landmarks.landmark[index].x * width)
                            y = int(hand_landmarks.landmark[index].y * height)
                            coordinates_fb.append([x, y])
                        # Obtener puntos de los pulgares
                        for index in thumb_points:
                            x = int(hand_landmarks.landmark[index].x * width)
                            y = int(hand_landmarks.landmark[index].y * height)
                            coordinates_thumb.append([x, y])

                        # nx, ny = palm_centroid(coordinates_palm)

                        ################### Calculos para el cierre de la mano ##################
                        #############
                        # Pulgar
                        p1 = np.array(coordinates_thumb[0])
                        p2 = np.array(coordinates_thumb[1])
                        p3 = np.array(coordinates_thumb[2])

                        l1 = np.linalg.norm(p2 - p3)
                        l2 = np.linalg.norm(p1 - p3)
                        l3 = np.linalg.norm(p1 - p2)

                        # Calcular el angulo
                        angle = degrees(
                            acos((l1**2 + l3**2 - l2**2)/(2 * l1 * l3)))
                        thumb_finger = np.array(False)
                        if angle > 150:
                            thumb_finger = np.array(True)

                        ####################

                        # Indice, medio, anular y meñique
                        nx, ny = palm_centroid(coordinates_palm)
                        cv2.circle(frame, (nx, ny), 3, (0, 255, 0), 2)
                        coordinates_centroid = np.array([nx, ny])
                        coordinates_ft = np.array(coordinates_ft)
                        coordinates_fb = np.array(coordinates_fb)

                        # Distancias
                        d_centrid_ft = np.linalg.norm(
                            coordinates_centroid - coordinates_ft, axis=1)
                        d_centrid_fb = np.linalg.norm(
                            coordinates_centroid - coordinates_fb, axis=1)
                        dif = d_centrid_ft - d_centrid_fb
                        fingers = dif > 0
                        fingers = np.append(thumb_finger, fingers)
                        # print(fingers)
                        cerrado = not np.all(fingers)

                        #########################################################################

                        # cv2.circle(frame, (nx, ny),3 ,(0, 255, 0), 2)
                        coordinates_centroid = np.array([nx, ny])

                        # Calculo de grados...
                        x_c = center[0]
                        y_c = center[1]
                        x_p = coordinates_centroid[0]
                        y_p = coordinates_centroid[1]
                        x_cercano = x_c
                        y_cercano = y_c

                        # Resolver la ecuación para x y y
                        distancia_superior = abs(y_p - (y_c + radio))
                        distancia_derecha = abs(x_p - (x_c + radio))
                        distancia_inferior = abs(y_p - (y_c - radio))
                        distancia_izquierda = abs(x_p - (x_c - radio))

                        # Encontrar la orilla más cercana
                        orilla_mas_cercana = np.argmin(
                            [distancia_superior, distancia_derecha, distancia_inferior, distancia_izquierda])
                        direccion = ""
                        # Calcular el punto más cercano en la orilla más cercana
                        if orilla_mas_cercana == 0:  # Orilla Inferior
                            x_cercano = x_c
                            y_cercano = y_c + radio
                            direccion = "Inferior"

                        elif orilla_mas_cercana == 1:  # Orilla derecha
                            x_cercano = x_c + radio
                            y_cercano = y_c
                            direccion = "Derecha"
                        elif orilla_mas_cercana == 2:  # Orilla Superior
                            x_cercano = x_c
                            y_cercano = y_c - radio
                            direccion = "Superior"
                        else:  # Orilla izquierda
                            x_cercano = x_c - radio
                            y_cercano = y_c
                            direccion = "Izquierda"
                       
                        rangex1 = (width/2)+(width*0.1)
                        rangex2 = (width/2)-(width*0.1)
                        rangey1 = (height/2)+(height*0.1)
                        rangey2 = (height/2)-(height*0.1)


                        if cerrado:
                            mask = close_hand_resized != 255
                            mask = mask[:close_hand_resized.shape[0], :close_hand_resized.shape[1]]
                            frame[0:close_hand_resized.shape[0], 0:close_hand_resized.shape[1]][mask] = close_hand_resized[mask]
                        else:
                            mask = open_hand_resized != 255
                            mask = mask[:open_hand_resized.shape[0], :open_hand_resized.shape[1]]
                            frame[0:open_hand_resized.shape[0], 0:open_hand_resized.shape[1]][mask] = open_hand_resized[mask]

                        cv2.line(frame, (int(rangex1), int( rangey1)), (int(rangex2), int( rangey1)), (0, 255, 0), 2)
                        cv2.line(frame, (int(rangex1), int( rangey2)), (int(rangex2), int( rangey2)), (0, 255, 0), 2)
                        cv2.line(frame, (int(rangex1), int(rangey1)), (int(rangex1), int(rangey2)), (0, 255, 0), 2)
                        cv2.line(frame, (int(rangex2), int(rangey1)), (int(rangex2), int(rangey2)), (0, 255, 0), 2)
                        if not( (x_p < rangex1 and x_p > rangex2) and  (y_p < rangey1 and y_p > rangey2)):
                            # Dibuja una linea desde el centro de la mano hasta el borde
                            cv2.line(frame, (int(x_p), int(y_p)), (int(x_cercano), int(y_cercano)), (0, 255, 0), lengthCenterLine)
                        else: 
                            direccion = ""
                        self.press_key_(direccion)

                        # Pinta los puntos de la mano
                        if printHand:
                            mp_drawing.draw_landmarks(
                                frame,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style()
                            )

                        # La variable direccion tiene la orientacion hacia donde vamos,
                        # La variable cerrado nos indica si tenemos la mano cerrada
                else:
                    self.liberarTecla("")
                
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()




    
    def press_key_(self,direction):
        if player is not None:
            if not direction == "":
                event_right_down = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
            else:
                event_right_down = pygame.event.Event(pygame.KEYUP, key=pygame.K_d)
            pygame.event.post(event_right_down)
            player.input("Desde movimiento")
            player.update_direction_from_camera(direction)

    def liberarTecla(self,direction):
        event_right_up = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
        try:
            pygame.event.post(event_right_up)
            player.input("Desde movimiento")
            player.update_direction_from_camera(direction)
        except pygame.error:
            pass


    def press_key_right(self):
        event_right_down = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
        pygame.event.post(event_right_down)
        player.input("Desde movimiento")
        

    def release_key(self,key):
        event = pygame.event.Event(pygame.KEYUP, key=pygame.key.key_code(key), mod=pygame.KMOD_NONE)
        pygame.event.post(event)


# if __name__ == "__main__":
#     movimiento = camara(None)
#     t = threading.Thread(target=movimiento.init, args=(False, 1, 1))
#     t.start()
