import cv2
from ultralytics import YOLO


# from Movement import Movement


class Detection_object:
    def __init__(self):
        self.coordinate_x = 0
        self.width = 320
        self.box_size = 20
        # self.m = Movement()
        self.for_send = ""
        self.last_move = None

    def get_coordinate_from_model(self):

        cap = cv2.VideoCapture("http://192.168.2.166:8080/?action=stream")
        # cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video stream.")
            exit()
        model = YOLO('best.pt')
        while True:
            ret, frame = cap.read()
            self.width = frame.shape[1] // 2
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            if not ret:
                print("Failed to grab frame")
                break
            flag = 0
            # Perform object detection
            results = model(frame)
            for box in results[0].boxes:
                flag = 1
                b = box.xyxy[0]
                c = box.cls
                item = None
                if c == 0:
                    item = 'ball'
                elif c == 3:
                    item = 'cube'
                left, top, right, bottom = b
                self.box_size = int(right - left)
                self.coordinate_x = int((left + right) // 2)
                # print((left + right) // 2, (top + bottom) // 2, 'C:', c)
                if c == 0:
                    self.for_send = self.robot_take(self.coordinate_x, 100, item)
            if not flag:
                if self.last_move == 'Right':
                    self.for_send = self.robot_take(-1, 100)
                elif self.last_move == 'Left':
                    self.for_send = self.robot_take(1000, 100)
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

    def robot_take(self, coordinate_x, distance_ultrasonics, item):
        if item == 'cube':
            if self.box_size <= 30:
                epsilon = 0.2
            elif self.box_size <= 70:
                epsilon = 1
            elif self.box_size <= 100:
                epsilon = 1.3
            elif self.box_size <= 150:
                epsilon = 1.5
            elif self.box_size > 300:
                epsilon = 4
            else:
                epsilon = 2
            print(self.box_size)
            if self.width - coordinate_x > self.box_size // epsilon:
                print("Left")
                if coordinate_x != -1 and coordinate_x != 1000:
                    self.last_move = 'Left'
                return 'Left'
            elif self.width - coordinate_x < -(self.box_size // epsilon):
                print("Right")
                if coordinate_x != -1 and coordinate_x != 1000:
                    self.last_move = 'Right'
                return 'Right'
            elif distance_ultrasonics > 100:
                return 'Forwards'
            else:
                print("FUCK!")
                return str(self.box_size)

        elif item == 'ball':
            if self.box_size <= 30:
                epsilon = 0.2
            elif self.box_size <= 70:
                epsilon = 1
            elif self.box_size <= 100:
                epsilon = 1.3
            elif self.box_size <= 150:
                epsilon = 1.5
            elif self.box_size > 300:
                epsilon = 4
            else:
                epsilon = 2
            print(self.box_size)
            if self.width - coordinate_x > self.box_size // epsilon:
                print("Left")
                if coordinate_x != -1 and coordinate_x != 1000:
                    self.last_move = 'Left'
                return 'Left'
            elif self.width - coordinate_x < -(self.box_size // epsilon):
                print("Right")
                if coordinate_x != -1 and coordinate_x != 1000:
                    self.last_move = 'Right'
                return 'Right'
            elif distance_ultrasonics > 100:
                return 'Forwards'
            else:
                print("FUCK!")
                return str(self.box_size)
        else:
            return ''
    # elif command == 2:
    #     pass
    # elif command == 3:
    #     pass
    # elif command == 4:
    #     pass

# detection = Detection_object()
# detection.get_coordinate_from_model()
