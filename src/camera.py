import cv2
from threading import Thread, Lock

class Camera:
    last_frame = None
    last_ready = None
    lock = Lock()
    active = True

    def __init__(self, rtsp_link):
        capture = cv2.VideoCapture(rtsp_link)
        thread = Thread(target=self.rtsp_cam_buffer, args=(capture,), name="rtsp_read_thread")
        thread.daemon = True
        thread.start()

    def rtsp_cam_buffer(self, capture):
        while self.active:
            with self.lock:
                self.last_ready, self.last_frame = capture.read()


    def get_frame(self):
        if (self.last_ready is not None) and (self.last_frame is not None):
            return self.last_frame.copy()
        else:
            return None
    
    def stop(self):
        self.active = False