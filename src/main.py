import cv2
import json
import time

from ultralytics import YOLO

from alert_state import AlertState


video_path = "test.mp4"
model = YOLO("yolov8s.pt")
alert_state = AlertState(duration=3.0)

cap = cv2.VideoCapture(video_path)


with open("restricted_zones.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    alert_zone = tuple(data['сordinates'])


def alert(px, py, rect):
    x1, y1, x2, y2 = rect
    return x1 <= px <= x2 and y1 <= py <= y2

def main():
    i = 0
    if not cap.isOpened():
        print("Не удалось открыть видеофайл")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        i += 1
        if i % 10 != 0:
            continue

        results = model.predict(frame)
        annotated_frame = results[0].plot()

        for r in results:
            for box in r.boxes:
                cls = int(box.cls)
                if cls != 0:
                    continue

                x1b, y1b, x2b, y2b = map(int, box.xyxy[0])
                cx = int((x1b + x2b) / 2)
                cy = int((y1b + y2b) / 2)

                cv2.circle(annotated_frame, (cx, cy), 4, (255, 0, 0), -1)

                if alert(cx, cy, alert_zone):
                    alert_state.trigger()
                    print("ALERT!")

            if alert_state.active():
                cv2.putText(annotated_frame, "ALERT!", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        x1, y1, x2, y2 = alert_zone
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imshow("Video", annotated_frame)
        if cv2.waitKey(25) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
