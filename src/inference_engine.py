from abc import ABC, abstractmethod

class InferenceEngine(ABC):

    @abstractmethod
    def predict(self, image):
        pass