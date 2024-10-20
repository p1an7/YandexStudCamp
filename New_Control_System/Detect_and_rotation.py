import cv2
from ultralytics import YOLO

#from Movement import Movement


class Detection_object:
    def __init__(self):
        self.coordinate_x = 0
        self.width = 320
        self.box_size = 20
        #self.m = Movement()
        self.for_send = ""

    def get_coordinate_from_model(self):

        cap = cv2.VideoCapture("http://192.168.2.166:8080/?action=stream")

        if not cap.isOpened():
            print("Error: Could not open video stream.")
            exit()
        model = YOLO('best-3.pt')
        while True:
            ret, frame = cap.read()
            self.width = frame.shape[1] // 2
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            if not ret:
                print("Failed to grab frame")
                break

            # Perform object detection
            results = model(frame)
            for box in results[0].boxes:
                b = box.xyxy[0]
                c = box.cls
                left, top, right, bottom = b
                self.box_size = right - left
                self.coordinate_x = int((left + right) // 2)
                print((left + right) // 2, (top + bottom) // 2, 'C:', c)
                self.for_send = self.robot_take(self.coordinate_x, 100)
            # Annotate the frame with detection results
            annotated_frame = results[0].plot()

            # Display the frame
            cv2.imshow('YOLO Object Detection', annotated_frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release resources
        cap.release()
        cv2.destroyAllWindows()

    def robot_take(self, coordinate_x, distance_ultrasonics):
        if self.width - coordinate_x > self.box_size // 2:
            return 'Left'
        elif self.width - coordinate_x < self.box_size // 2:
            return 'Right'
        elif distance_ultrasonics > 100:
            return 'Forwards'
        else:
            print("FUCK!")
            return True

    # elif command == 2:
    #     pass
    # elif command == 3:
    #     pass
    # elif command == 4:
    #     pass


'''detection = Detection_object()
detection.get_coordinate_from_model()
'''