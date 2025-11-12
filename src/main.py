import cv2

def main(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Не удалось открыть видеофайл")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video", frame)


        if cv2.waitKey(25) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = "test.mp4"
    main(video_path)
