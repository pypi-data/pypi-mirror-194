"""
The class Cam initializes an instance of
the class with a given model. It computes guided gradients and weights,
then overlays the computed CAM heatmap on the input image to generate
the final heatmap.
"""

# Import libraries
import tensorflow as tf
import numpy as np
import cv2

from Utils import normalize

class GradCam:
    """
    A class for generating class activation maps
    for image classification models.
    """
    def __init__(self, model):
        """
        Initialize the Cam class with a given model and target class index.

        :param model: A Keras model instance
        :param class_idx: An integer representing the target class index
        """
        self.model = model
        self.layers = [layer.name for layer in reversed(model.layers) if
                       len(layer.output_shape) == 4 and
                       (layer.__class__.__name__ == 'ReLU' or \
                         isinstance(layer, tf.keras.layers.Conv2D))]


    def _get_grad_model(self, layer_name=None):
        """
        Get the model used for gradient computations.

        Returns:
            tf.keras.Model: The model to use for gradient computations.
        """
        if not layer_name:
            layer_name = self.layers[0]
        gradmodel = tf.keras.Model(inputs=self.model.inputs,
                                outputs=[self.model.get_layer(layer_name).output,\
                                self.model.output])
        return gradmodel

    def _compute_guided_grads(self, convOutputs, grads):
        """
        Computes guided gradients using the provided inputs.

        :param convOutputs: The output activations from the desired layer.
        :param grads: The gradients with respect to the loss.

        Returns:
            numpy.ndarray: The guided gradients.
        """
        castConvOutputs = tf.cast(convOutputs > 0, "float32")
        castGrads = tf.cast(grads > 0, "float32")
        guidedGrads = castConvOutputs * castGrads * grads
        return guidedGrads

    def _compute_weights(self, guidedGrads):
        """
        Computes the weights for the guided gradients.

        :param guidedGrads: The guided gradients to use for weight computation.

        Returns:
            numpy.ndarray: The computed weights.
        """
        return tf.reduce_mean(guidedGrads, axis=(0, 1))

    def _resize(self, img, cam):
        """
        Resizes the CAM heatmap to match the size of the input image.

        :param img: The input image.
        :param cam: The CAM heatmap.

        Returns:
            numpy.ndarray: The resized CAM heatmap.
        """
        (w, h) =  (img.shape[2], img.shape[1])
        heatmap = cv2.resize(cam.numpy(), (w, h))
        return heatmap


    def _get_pred_index(self, preds, n):
        """
        Get the class index for the top n prediction.

        :param preds: An array of predictions
        :param index: An integer representing the position of the prediction in the sorted array

        :return: An integer representing the class index of the top n prediction
        """
        classIdx = np.argsort(preds[0])[::-1]
        return classIdx[n]



    def compute_map(self, img, n, layer_name=None):
        """
        Computes the Grad-CAM visualization for the input image and target class index.

        :param img: A numpy array representing the input image.
        :param layer_name: (Optional) The name of the layer to use for the Grad-CAM computation.
                           If not specified, the first layer will be used.

        Returns:
            numpy.ndarray: A numpy array of the Grad-CAM heatmap.
        """
        # expand dims (1, n, m, 3)
        img = np.expand_dims(img, axis=0)

        # Start recording the gradient computation
        with tf.GradientTape() as tape:

            # Cast the input image to a tensor and pass it through the model
            img_cast = tf.cast(img, tf.float32)
            (convOutputs, preds) = self._get_grad_model(layer_name)(img_cast)

            # Calculate the loss for the target class
            loss = preds[:, self._get_pred_index(preds, n)]

        # Compute the gradient of the loss with respect to the model outputs
        grads = tape.gradient(loss, convOutputs)

        # Compute the guided gradients
        guidedGrads = self._compute_guided_grads(convOutputs, grads)[0]

        # Compute the weights for each feature map
        convOutputs = convOutputs[0]
        weights = self._compute_weights(guidedGrads)

        # Calculate the Grad-CAM heatmap
        cam = tf.reduce_sum(tf.multiply(weights, convOutputs), axis=-1)

        # Resize the heatmap to match the size of the input image
        heatmap = self._resize(img_cast, cam)

        # Normalize the heatmap between 0 and 1
        heatmap_norm = normalize(heatmap)

        # Return the heatmap as a numpy array with values in the range [0, 255]
        return (heatmap_norm * 255).astype("uint8")


if __name__ == "__main__":
    pass