import torch
from utils import get_logger, download_model
import torchvision.transforms as transforms
import time
from inference_engine import InferenceEngine
import os

LOGGER = get_logger()

class InferenceTorchScript(InferenceEngine):

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
        download_model(os.environ.get("TORCHSCRIPT_MODEL_URL"), "model.pt")
        self.__model = torch.jit.load('model.pt', map_location=torch.device('cpu'))
        LOGGER.info("Loading model... done")

        # disable dropout and batchnorm
        self.__model.eval()

        # pass dummy input to warm up the model
        LOGGER.info("Warming up model...")
        self.__model(torch.randn(1, 3, 224, 224))
        LOGGER.info("Warming up model... done")

    def __preprocess(self, image):
        tensor = self.transform(image)
        tensor = tensor.view(1, 3, 224, 224)

        return tensor

    def predict(self, image):
        start_time = time.time()
        input_tensor = self.__preprocess(image)

        with torch.no_grad():
            self.__model.eval()

            # forward input
            output = self.__model(input_tensor)
            
            # log probabilities
            ps = torch.exp(output) 

            return ps[0].tolist(), time.time() - start_time