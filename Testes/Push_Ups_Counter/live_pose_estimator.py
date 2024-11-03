import mediapipe as mp
from mediapipe.tasks import python
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import numpy as np

file_name = "landmark_test.mp4"
model_path = 'pose_landmarker_lite.task'

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Função callback para lidar com os resultados de forma assíncrona
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global annotated_image
    annotated_image = draw_landmarks_on_image(output_image.numpy_view(), result)
    # Exibe a imagem anotada com as landmarks
    cv2.imshow("Frame", annotated_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Se 'q' for pressionado, encerra a execução
        cap.release()
        cv2.destroyAllWindows()

# Configura o PoseLandmarker para o modo LIVE_STREAM
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result  # callback para processar os resultados
)

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Desenha as landmarks
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) 
            for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )
    return annotated_image

# Inicializa o PoseLandmarker em modo LIVE_STREAM
with PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)  # Acessa a câmera ao vivo

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Envia o quadro para o landmarker de forma assíncrona
            landmarker.detect_async(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
        else:
            break

    cap.release()
    cv2.destroyAllWindows()