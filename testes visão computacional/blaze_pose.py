import mediapipe as mp
import cv2 as cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
# para imagens estáticas

with mp_pose.Pose(
    static_image_mode = True,
    model_complexity = 2,
    min_detection_confidence = 0.5) as pose:
    image = cv2.imread("testes visão computacional\description.jpg")
    image_height, image_width, _ = image.shape
    #converte a imagem BGR em RGB antes de processar
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #desenha as landmarks na imagem
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imwrite(r"testes visão computacional\description.jpg", annotated_image)
