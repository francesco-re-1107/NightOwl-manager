from PIL import Image
import requests
from threading import Thread
from utils import get_logger
import time
from camera import Camera
from inference_torchscript import InferenceTorchScript
from inference_onnx import InferenceONNX
import os
from utils import to_int, to_float
try:
    trigger = lambda: print("Trigger not defined")
    from trigger import trigger
except Exception as e:
    trigger = lambda: print("Trigger error:", e )
    print(e)

LOGGER = get_logger()
STREAM_URL = os.environ.get("STREAM_URL") or exit("STREAM_URL not specified")
MOVING_AVG_WINDOW = to_int(os.environ.get("MOVING_AVG_WINDOW"), 10)
COOLDOWN_TIME = to_int(os.environ.get("COOLDOWN_TIME"), 60 * 20) # 20 minutes
TRIGGER_THRESHOLD = to_float(os.environ.get("TRIGGER_THRESHOLD"), 1.9)

class Analyzer:

    def __init__(self):
        self.enabled = False
        self.inference_history = []
        self.trigger_datetimes = []

        if os.environ.get("ONNX_MODEL_URL"):
            self.inference_engine = InferenceONNX()
        elif os.environ.get("TORCHSCRIPT_MODEL_URL"):
            self.inference_engine = InferenceTorchScript()
        else:
            raise Exception("No model specified")

        self.last_trigger = None

    def __get_inference(self, snapshot):
        return self.inference_engine.predict(Image.fromarray(snapshot))

    def __start(self):
        cam = Camera(STREAM_URL)

        while self.enabled:
            # cooldown
            if self.last_trigger and time.time() - self.last_trigger < COOLDOWN_TIME:
                time.sleep(5)
                continue

            snapshot = cam.get_frame()

            if snapshot is None:
                time.sleep(0.1)
                continue

            probabilities, inf_time = self.__get_inference(snapshot)
            val = probabilities[1] * 1 + probabilities[2] * 2

            self.inference_history.append(val)

            if len(self.inference_history) > MOVING_AVG_WINDOW:
                m_avg = sum(self.inference_history[-MOVING_AVG_WINDOW:]) / MOVING_AVG_WINDOW
                
                LOGGER.debug(f"Current val {val:4.2f} | Moving avg {m_avg:4.2f} | Inf, time {(inf_time*1000):4.1f} ms")

                if m_avg > TRIGGER_THRESHOLD:
                    LOGGER.warning("Triggered")

                    self.trigger_datetimes.append(time.time())
                    self.last_trigger = time.time()
                    trigger()
                    self.end()

        cam.stop()

    def start(self):
        self.enabled = True
        Thread(target=self.__start).start()

    def end(self):
        self.enabled = False
        self.inference_history = []