


#INCOMPLETO


import mediapipe as mp
from mediapipe.tasks import python
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import numpy as np
import threading
import queue
import math

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

class PersonalAI:
    def __init__(self, file_name="landmark_test.mp4"):
        self.file_name = file_name
        self.model_path = 'pose_landmarker_full.task'
        self.image_q = queue.Queue()
        self.options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result
        )

    def print_result(self, result, output_image, timestamp_ms):
        # Exibe apenas o timestamp e a quantidade de landmarks para reduzir impressões
        if result.pose_landmarks:
            print(f'Timestamp: {timestamp_ms} ms, Landmarks detected: {len(result.pose_landmarks)}')
        
        # Converte o output_image para formato OpenCV se não estiver nulo
        if output_image is not None:
            frame = output_image.numpy_view()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Conversão para BGR
            self.image_q.put((frame, result, timestamp_ms))  # Coloca na fila

    def draw_landmarks_on_image(self, frame, detection_result):
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(frame)

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

    def process_video(self, draw, display):
        with PoseLandmarker.create_from_options(self.options) as landmarker:
            cap = cv2.VideoCapture(0)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            calc_ts = 0

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    self.image_q.put((None, None, "done"))
                    break

                # Converte o quadro para o formato esperado pelo MediaPipe
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                calc_ts += int(1000 / fps)  # Calcula o timestamp para o quadro atual
                
                # Detecta as landmarks de forma assíncrona para um fluxo ao vivo
                landmarker.detect_async(mp_image, calc_ts)

                # Pega o frame da fila de exibição (se draw estiver ativo)
                if not self.image_q.empty():
                    frame, detection_result, _ = self.image_q.get()

                    if draw and detection_result:
                        frame = self.draw_landmarks_on_image(frame, detection_result)

                    # Exibe o quadro atualizado
                    if display:
                        cv2.imshow("Frame", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

            cap.release()
            cv2.destroyAllWindows()
            self.image_q.put((None, None, "done"))

    def find_angle(self, landmarks, p1, p2, p3):
        land = landmarks.pose_landmarks[0]
        x1, y1 = (land[p1].x, land[p1].y)
        x2, y2 = (land[p2].x, land[p2].y)
        x3, y3 = (land[p3].x, land[p3].y)
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        return angle

    def run(self, draw=True, display=False):
        t1 = threading.Thread(target=self.process_video, args=(draw, display))
        t1.start()

if __name__ == "__main__":
    personalAI = PersonalAI()
    personalAI.process_video(True, True)
