import cv2
from ultralytics import YOLO

video_path = "test.mp4"
model = YOLO("yolov8s.pt")
cap = cv2.VideoCapture(video_path)
exit_zone = (930, 400, 1250, 700)


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

        x1, y1, x2, y2 = exit_zone

        cv2.rectangle(annotated_frame,  (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imshow("Video", annotated_frame)


        if cv2.waitKey(25) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
