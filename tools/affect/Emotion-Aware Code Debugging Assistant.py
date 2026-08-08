import cv2
import time
import json
import math
import argparse
import numpy as np
import mediapipe as mp
from deepface import DeepFace

FRUSTRATION_THRESHOLD = 0.6
BLINK_EAR_THRESHOLD = 0.19
BLINK_CONSEC_FRAMES = 2
LOG_FILE = "frustration_log.json"
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
LEFT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(pts):
    A = math.dist(pts[1], pts[5])
    B = math.dist(pts[2], pts[4])
    C = math.dist(pts[0], pts[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_blink_and_headpose_and_distance(face_landmarks, image_w, image_h):
    mesh_points = np.array(
        [(int(p.x * image_w), int(p.y * image_h), p.z) for p in face_landmarks.landmark]
    )

    left_eye_pts = [(mesh_points[i][0], mesh_points[i][1]) for i in LEFT_EYE_LANDMARKS]
    right_eye_pts = [(mesh_points[i][0], mesh_points[i][1]) for i in RIGHT_EYE_LANDMARKS]

    left_ear = eye_aspect_ratio(left_eye_pts)
    right_ear = eye_aspect_ratio(right_eye_pts)
    ear = (left_ear + right_ear) / 2.0

    nose = mesh_points[1]
    chin = mesh_points[152]
    head_tilt = math.degrees(math.atan2(chin[1] - nose[1], chin[0] - nose[0]))

    dist_face = math.dist((nose[0], nose[1]), (chin[0], chin[1]))

    return ear, head_tilt, dist_face

def get_emotion(frame, face_box):
    x, y, w, h = face_box
    x, y = max(0, x), max(0, y)
    roi = frame[y:y+h, x:x+w]
    if roi.size == 0:
        return "neutral", 0.0
    try:
        result = DeepFace.analyze(
            roi,
            actions=['emotion'],
            enforce_detection=False
        )
        # DeepFace returns a list of dicts in new versions [web:62]
        res0 = result[0] if isinstance(result, list) else result
        dominant = res0['dominant_emotion']
        score = res0['emotion'][dominant] / 100.0
        return dominant, score
    except Exception:
        return "neutral", 0.0

def map_features_to_frustration(emotion, emotion_score, blink_rate, head_tilt, face_size_norm):
    score = 0.0

    # emotions
    if emotion in ["angry", "sad", "fear", "disgust"]:
        score += 0.4 * emotion_score
    elif emotion == "happy":
        score -= 0.2 * emotion_score

    if blink_rate > 25:
        score += 0.2
    elif blink_rate < 5:
        score += 0.1

    if abs(head_tilt) > 20:
        score += 0.1

    if face_size_norm > 0.12:
        score += 0.2

    return max(0.0, min(1.0, score))

def load_log():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_log(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Current code file name", default="unknown_file.py")
    args = parser.parse_args()
    file_name = args.file

    cap = cv2.VideoCapture(0)

    blink_counter = 0
    frame_counter = 0
    consec_closed = 0
    start_time = time.time()
    last_minute_time = start_time
    blinks_last_minute = 0
    blink_rate = 0

    log_data = load_log()
    if file_name not in log_data:
        log_data[file_name] = []

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_counter += 1

            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            frustration_score = 0.0
            display_text = "No face"
            emotion = "neutral"

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                ear, head_tilt, face_size = get_blink_and_headpose_and_distance(face_landmarks, w, h)

                if ear < BLINK_EAR_THRESHOLD:
                    consec_closed += 1
                else:
                    if consec_closed >= BLINK_CONSEC_FRAMES:
                        blink_counter += 1
                        blinks_last_minute += 1
                    consec_closed = 0

                # Blink rate per minute
                now = time.time()
                if now - last_minute_time >= 60:
                    blink_rate = blinks_last_minute / ((now - last_minute_time) / 60.0)
                    last_minute_time = now
                    blinks_last_minute = 0

                # Rough face box for emotion ROI
                xs = [int(p.x * w) for p in face_landmarks.landmark]
                ys = [int(p.y * h) for p in face_landmarks.landmark]
                x_min, x_max = max(min(xs), 0), min(max(xs), w-1)
                y_min, y_max = max(min(ys), 0), min(max(ys), h-1)
                face_box = (x_min, y_min, x_max - x_min, y_max - y_min)

                emotion, emo_score = get_emotion(frame, face_box)

                # normalize face size by frame area
                face_size_norm = (face_box[2] * face_box[3]) / float(w * h + 1e-6)

                frustration_score = map_features_to_frustration(
                    emotion, emo_score, blink_rate, head_tilt, face_size_norm
                )

                # draw overlay
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(frame, f"Emotion: {emotion}",
                            (x_min, y_min - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.putText(frame, f"EAR: {ear:.2f}",
                            (x_min, y_min - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                cv2.putText(frame, f"Blink/min: {blink_rate:.1f}",
                            (x_min, y_min - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

                bar_width = int(200 * frustration_score)
                cv2.rectangle(frame, (10, 10), (10 + 200, 30), (50, 50, 50), -1)
                cv2.rectangle(frame, (10, 10), (10 + bar_width, 30), (0, 0, 255), -1)
                cv2.putText(frame, f"Frustration: {frustration_score:.2f}",
                            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                display_text = f"{emotion}, frus={frustration_score:.2f}"

                # trigger “help” if frustration high
                if frustration_score > FRUSTRATION_THRESHOLD:
                    cv2.putText(frame, "SUGGEST BREAK / SHOW DOCS",
                                (50, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

                # log every 5 seconds
                if now - start_time > 5:
                    log_data[file_name].append({
                        "timestamp": now,
                        "emotion": emotion,
                        "frustration": float(frustration_score),
                        "blink_rate": float(blink_rate),
                        "head_tilt": float(head_tilt),
                        "face_size_norm": float(face_size_norm)
                    })
                    save_log(log_data)
                    start_time = now

            cv2.putText(frame, display_text, (10, h - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("Emotion-Aware Debugging Assistant", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
