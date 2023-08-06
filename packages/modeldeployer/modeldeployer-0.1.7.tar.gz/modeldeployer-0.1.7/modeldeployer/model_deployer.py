from typing import List
from .exceptions import IsNotList, IsNotFunction


class ModelDeployer:
    def __init__(self, features: List[str] = None, predict=None, calibrate=None):
        if isinstance(features, list):
            self.features = features
        else:
            raise IsNotList(message="argument 'features' is not a list!")
        if callable(predict):
            self.predict = predict
        else:
            raise IsNotFunction(message="argument 'predict' is not a function!")
        if callable(calibrate):
            self.calibrate = calibrate
        else:
            raise IsNotFunction(message="argument 'calibrate' is not a function!")
