import logging
import math
from scipy.spatial import distance as dist
import os.path
from typing import Union, Tuple

import cv2
import mediapipe as mp
from logging.handlers import TimedRotatingFileHandler

mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh


class MediapipeHelper:
    def __init__(self):
        pass

    def normalized_to_pixel_coordinates(self,
                                        normalized_x: float, normalized_y: float, image_width: int,
                                        image_height: int) -> Union[None, Tuple[int, int]]:
        """Converts normalized value pair to pixel coordinates."""

        # Checks if the float value is between 0 and 1.
        def is_valid_normalized_value(value: float) -> bool:
            return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                              math.isclose(1, value))

        if not (is_valid_normalized_value(normalized_x) and
                is_valid_normalized_value(normalized_y)):
            # TODO: Draw coordinates even if it's outside of the image bounds.
            return None
        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px

    def eye_aspect_ratio(self, eye, eyePoints):
        try:
            # compute the euclidean distances between the two sets of
            # vertical eye landmarks (x, y)-coordinates
            A = dist.euclidean(eye[eyePoints[1]], eye[eyePoints[5]])
            B = dist.euclidean(eye[eyePoints[2]], eye[eyePoints[4]])
            # compute the euclidean distance between the horizontal
            # eye landmark (x, y)-coordinates
            C = dist.euclidean(eye[eyePoints[0]], eye[eyePoints[3]])
            # compute the eye aspect ratio
            ear = (A + B) / (2.0 * C)
            # return the eye aspect ratio
            return ear
        except Exception as error:
            print(f"EAR error: {error}")
            # exception_log_function(sys.exc_info(), f"Eye except ratio (handled): {error}")
            return 1


class MediapipeFaceInfo:
    def __init__(self, check_for_landmark=True, face_det_conf=0.5, face_padding=15, mesh_det_conf=0.5, mesh_track_conf=0.5):
        self.det_conf = face_det_conf
        self.padding = face_padding
        self.check_for_landmark = check_for_landmark
        self.face_detection_model = mp_face_detection.FaceDetection(model_selection=1,
                                                                    min_detection_confidence=face_det_conf)
        self.face_mesh_model = mp_face_mesh.FaceMesh(max_num_faces=1,
                                                     refine_landmarks=True,
                                                     min_detection_confidence=mesh_det_conf,
                                                     min_tracking_confidence=mesh_track_conf)
        self.__VISIBILITY_THRESHOLD = 0.6
        self.__PRESENCE_THRESHOLD = 0.6
        self.__mediapipe_helper = MediapipeHelper()
        self.__leftEye = [263, 387, 385, 362, 380, 373]
        self.__rightEye = [133, 158, 160, 33, 144, 153]

    def mediapipe_face_mesh(self, frame):
        face_mesh_landmarks = None
        idx_to_coordinates = {}
        try:
            results = self.face_mesh_model.process(frame)
            image_rows, image_cols, _ = frame.shape

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    face_mesh_landmarks = face_landmarks.landmark
                    for idx, landmark in enumerate(face_mesh_landmarks):
                        if ((landmark.HasField('visibility') and
                             landmark.visibility < self.__VISIBILITY_THRESHOLD) or
                                (landmark.HasField('presence') and
                                 landmark.presence < self.__PRESENCE_THRESHOLD)):
                            continue
                        landmark_px = self.__mediapipe_helper.normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                                                              image_cols, image_rows)
                        if landmark_px:
                            idx_to_coordinates[idx] = landmark_px
        except Exception as error:
            print(f"Error: {error}")
        return face_mesh_landmarks, idx_to_coordinates

    def get_all_faces_bbox(self, original_frame):
        detected_faces = []
        try:
            frame = original_frame.copy()
            # To improve performance, optionally mark the image as not writeable to
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_height, image_width, _ = frame.shape
            detection_results = self.face_detection_model.process(frame)
            if detection_results:
                for detection in detection_results:
                    location = detection.location_data.relative_bounding_box

                    x = location.xmin  # normalized coordinates
                    y = location.ymin
                    w = location.width
                    h = location.height

                    x_px = min(math.floor(x * image_width), image_width - 1)  # denormalized coordinates
                    y_px = min(math.floor(y * image_height), image_height - 1)
                    w_px = min(math.floor(w * image_width), image_width - 1)
                    h_px = min(math.floor(h * image_height), image_height - 1)

                    # cv2.rectangle(baseimage,(x_px,y_px),(x_px+w_px,y_px+h_px),color=(255,0,255),thickness=1)
                    face = (x_px, y_px, w_px, h_px)
                    face_x, face_y, face_w, face_h = face
                    face_x = max(face_x, 0)
                    face_y = max(face_y, 0)
                    face_left = face_x
                    face_right = face_x + face_w
                    face_top = face_y
                    face_bottom = face_y + face_h

                    padded_face_left = max(int(face_left - self.padding), 0)
                    padded_face_top = max(int(face_top - self.padding), 0)
                    padded_face_right = min(int(face_right + self.padding), image_width)
                    padded_face_bottom = min(int(face_bottom + self.padding), image_height)

                    # cropped_face_only = for_face_frame[face_top:face_bottom, face_left:face_right]

                    # padded_face_left = face_left
                    # padded_face_top = face_top
                    # padded_face_right = face_right
                    # padded_face_bottom =face_bottom

                    if not self.check_for_landmark:
                        direct_face_points = [padded_face_left, padded_face_top, padded_face_right,
                                              padded_face_bottom]
                        faces_found.append(direct_face_points)

                        # do not go further to check face landmarks like eyes, nose, ears, etc
                        continue

                    cropped_face_only = frame[padded_face_top:padded_face_bottom,
                                        padded_face_left:padded_face_right]

                    shape, landmark_pos = self.mediapipe_face_mesh(cropped_face_only)
                    if shape:
                        leftEAR = self.__mediapipe_helper.eye_aspect_ratio(landmark_pos, self.__leftEye)
                        rightEAR = self.__mediapipe_helper.eye_aspect_ratio(landmark_pos, self.__rightEye)

                        # if leftEAR or rightEAR == 1 then there must be some value missing in eye points
                        if leftEAR == 1 or rightEAR == 1:
                            continue

                        # else the face is ok to be processed
                        else:
                            cropped_face_points = [padded_face_left, padded_face_top, padded_face_right,
                                                   padded_face_bottom]
                            # box = cropped_face_points * np.array([image_width, image_height, image_width, image_height])
                            # found_face_detections.append(box.astype("int"))
                            box = cropped_face_points
                            detected_faces.append(box)
        except Exception as error:
            print(f"Error in finding face: {error}")
            detected_faces = []

        return detected_faces
