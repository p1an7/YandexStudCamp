import cv2
import numpy as np
from datetime import datetime


def segment_cube(frame):
    def show(images):
        size = (900, 600)
        for i, image in enumerate(images):
            window_name = f'window {i}'
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, *size)
            cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def find_color(image, lower, upper, color='bgr', show_image=True):
        image = cv2.copyMakeBorder(image, 1, 1, 1, 1,
                                  cv2.BORDER_CONSTANT, None, [255, 255, 255])
        original_image = image.copy()  # копируем изображение
        image = image.copy()

        if color == 'hsv':  # если цветовая модель hsv
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # переводим в hsv
        if color == 'gray':  # если цветовая модель gray
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # переводим в gray
        lower = np.array(lower)  # нижняя граница
        upper = np.array(upper)  # верхняя граница
        mask = cv2.inRange(image, lower, upper)  # создаем маску
        if color == 'gray':
            image = cv2.bitwise_and(image, image, mask=mask)  # применяем маску
        elif color == 'hsv':
            image[mask == 0] = [0, 0, 255]
        else:
            image[mask == 0] = [255, 255, 255]
        if color == 'hsv':
            image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)  # переводим в bgr
        if color == 'gray':
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if show_image:
            show([original_image, image])  # выводим изображение
        return image

    img = find_color(frame, [0, 50, 100], [200, 200, 255], 'hsv', show_image=False)
    image = find_color(img, [0, 0, 100], [200, 255, 255], 'brg', show_image=False)

    def find_contours(image, show_image=False):
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        if show_image:
            show([image])
        return contours

    def binarize(image, show_image=False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if show_image:
            show([image, binary])
        return binary

    contours = find_contours(binarize(image, False), show_image=False)
    biggest = sorted(contours, key=cv2.contourArea, reverse=True)
    #cv2.drawContours(image, biggest, -1, (0, 255, 0), 3)
    #return image
    def create_mask(image, contours, show_image=False):
        mask = np.zeros_like(image)
        for contour in contours:
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        if show_image:
            show([mask])
        return mask

    mask = create_mask(binarize(image, False), biggest[1:5], show_image=False)
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=2)

    new_image = image.copy()

    new_image[dilated_mask == 0] = 255
    # return new_image
    def find_convex_hull(image, contour, show_image=False):
        hull = cv2.convexHull(contour)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(image, [hull], -1, (0, 255, 0), 3)
        if show_image:
            show([image])
        return hull

    try:
        hull = find_convex_hull(binarize(new_image, False), biggest[1], show_image=False)
    except:
        pass
    else:
        cv2.drawContours(frame, [hull], -1, (0, 255, 0), 3)
    finally:
        return frame


def main():
    # Create a VideoCapture object
    cap = cv2.VideoCapture('http://192.168.2.166:8080/?action=stream')
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture device.")
        return

    # Get the default frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Recording started. Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = segment_cube(frame)
            # Exit the loop when 'q' key is pressed
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Recording stopped by user.")
                break
        else:
            print("Error: Failed to read frame from camera.")
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
