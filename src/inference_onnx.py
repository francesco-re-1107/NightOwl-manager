import torch
from utils import get_logger, download_model
from torchvision.models import resnet50
import torchvision.transforms as transforms
import time
from inference_engine import InferenceEngine
import onnxruntime
import os

LOGGER = get_logger()

class InferenceONNX(InferenceEngine):

    def __init__(self):
        self.__prepare_model()

        # setup transforms
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def __prepare_model(self):
        # load model
        LOGGER.info("Loading model...")
        download_model(os.environ.get("ONNX_MODEL_URL"), "model.onnx")
        self.ort_session = onnxruntime.InferenceSession("model.onnx")
        LOGGER.info("Loading model... done")

    def __to_numpy(self, tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    def __preprocess(self, image):
        tensor = self.transform(image)
        tensor = tensor.view(1, 3, 224, 224)

        return self.__to_numpy(tensor)

    def predict(self, image):
        start_time = time.time()
        input_tensor = self.__preprocess(image)

        ort_outs = self.ort_session.run(None, {'input': input_tensor})
        output = ort_outs[0]

        # log probabilities
        ps = torch.exp(torch.from_numpy(output))

        return ps[0].tolist(), time.time() - start_time