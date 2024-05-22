from common_imports import cv2


class VideoFrameCounter:
    def __init__(self, video_path):
        self.video_path = video_path

    def count_frames(self):
        # Open the video file
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print("Error: Could not open video file.")
            return -1

        # Get the total number of frames in the video
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Release the video capture object
        cap.release()

        return frame_count
