"""
This code is a Python class that generates saliency maps for
image classification models. The class Saliencymap initializes
an instance of the class with an image classification model and
an input image. It uses Tensorflow to compute the gradients of
the prediction with respect to the input image and returns a
gradient saliency map.
"""
# Import libraries
import tensorflow as tf
import numpy as np
import cv2

from Utils import normalize

class SaliencyMap():
    """
    A class for generating saliency maps for image classification models.
    """

    def __init__(self, model, img):
        """
        Initialize an instance of the Saliencymap class.

        Parameters:
        - model: The image classification model.
        - img: The input image.
        """
        self.model = model
        # Add an extra dimension to the input image
        self.img = np.expand_dims(img, axis=0)

    def _compute_grads(self):
        """
        Compute the gradients of the prediction with respect to the input image.
        """
        img = tf.Variable(self.img, dtype=float)

        with tf.GradientTape() as tape:
            # Get the predictions from the model
            preds = self.model(img)[0] # Nested list
            # Get the index of the class with the highest prediction
            classIdx = np.argsort(preds)[::-1]
            # Use the highest prediction as the loss
            loss = preds[classIdx[0]]
        # Compute the gradients of the loss with respect to the input image
        grads = tape.gradient(loss, img)

        return grads

    def gradient_saliency_map(self):
        """
        Generate the gradient saliency map.

        Returns:
        - The gradient saliency map.
        """
        # Compute the gradients of the prediction with respect to the input image
        grads = self._compute_grads()
        # Get the absolute values of the gradients
        grads_abs = np.abs(grads)
        # Find the maximum value along the last axis of the absolute gradients
        grad_max = np.max(grads_abs, axis=3)[0]
        # Normalize the gradient values
        grads_norm = normalize(grad_max)

        return grads_norm
    


if __name__ == "__main__":
    pass

