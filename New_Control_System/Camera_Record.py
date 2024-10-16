import cv2
import numpy as np
from datetime import datetime


def main():
    # Choose video source: 0 for webcam or provide a filename for a video file
    video_source = 0  # Set to 0 for webcam, or replace with 'video_filename.mp4' for a video file

    # Create a VideoCapture object
    cap = cv2.VideoCapture('http://192.168.2.166:8080/?action=stream')
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture device.")
        return

    # Get the default frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create a VideoWriter object
    # FourCC is a 4-byte code used to specify the video codec
    # You can change 'MJPG' to 'XVID', 'DIVX', etc., depending on your system
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    timestamp = datetime.now()

    out = cv2.VideoWriter(f'output{timestamp}.avi', fourcc, 20.0, (frame_width, frame_height))

    print("Recording started. Press 'q' to stop.")

    while True:
        ret, frame = cap.read()

        if ret:
            # Write the frame to the output file
            out.write(frame)

            # Display the frame (optional)
            cv2.imshow('Recording', frame)

            # Exit the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Recording stopped by user.")
                break
        else:
            print("Error: Failed to read frame from camera.")
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()