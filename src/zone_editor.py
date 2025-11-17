import cv2
import json

img = cv2.imread("media/frame.jpg")
clone = img.copy()
points = []

def zone_editor():
    def draw_rect(event, x, y, flags, param):
        global points, img

        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))

            if len(points) == 2:
                cv2.rectangle(img, points[0], points[1], (0, 0, 255), 2)
                cv2.imshow("Select zone", img)

    cv2.namedWindow("Select zone")
    cv2.setMouseCallback("Select zone", draw_rect)

    print("Кликни 2 раза — две точки прямоугольника (x1,y1 и x2,y2)")
    print("Нажми 's' чтобы сохранить зону, 'q' – выйти без сохранения")

    while True:
        cv2.imshow("Select zone", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s") and len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]

            zone = {"cordinates": [x1, y1, x2, y2]}

            with open("restricted_zones.json", "w", encoding="utf-8") as f:
                json.dump(zone, f, indent=4, ensure_ascii=False)

            print("Зона сохранена в restricted_zones.json")
            break

        if key == ord("q"):
            print("Выход без сохранения")
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    zone_editor()
