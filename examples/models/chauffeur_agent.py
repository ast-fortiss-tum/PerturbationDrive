from perturbationdrive import ADS

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import SGD
from typing import List, Any
from numpy import dtype, ndarray, uint8
import numpy as np
import os


class ChauffeurAgent(ADS):
    """
    Example agent using chauffeur architecture
    """

    def __init__(self, model_path: str = "./examples/models/chauffuer_90k_v1.h5"):
        if not (os.path.exists(model_path) and os.path.isfile(model_path)):
            print(f"{5 * '+'} Warning: ADS file does not exists {5 * '+'}")
        self.model = load_model(model_path, compile=False)
        print(f"Using model: {model_path}")
        use_adadelta = True
        optimizer = "adadelta" if use_adadelta else SGD(lr=0.0001, momentum=0.9)
        self.model.compile(loss="mse", optimizer=optimizer, metrics=["acc"])
        self.name = model_path.split("/")[-1].split(".")[0]

    def action(self, input: ndarray[Any, dtype[uint8]]) -> List:
        """
        Takes one action step given the input, here the input is a cv2 image.
        This method also contains the preparation for the underlying model
        """
        # adapt dtype of input
        img_arr = np.asarray(input, dtype=np.float32)
        # add batch dimension
        img_arr = img_arr.reshape((1,) + img_arr.shape)
        actions = self.model(img_arr, training=False)
        # deep copy action
        actions = actions.numpy().tolist()
        actions[0][0] = actions[0][0] * 2.2
        return actions

    def name(self) -> str:
        """
        Returns the name of the ADS
        """
        return self.name
