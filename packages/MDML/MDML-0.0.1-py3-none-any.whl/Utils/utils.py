import numpy as np
import keras
def normalize(arr):
    """
    Normalize an array between 0 and 1.

    Parameters:
    - arr: The input array.

    Returns:
    - The normalized array.
    """
    # Calculate the minimum and maximum values of the array
    min_values = np.min(arr)
    max_values = np.max(arr)
    # Normalize the array
    return (arr - min_values) / (max_values - min_values)

if __name__ == '__main__':
    pass

def write_to_file(filename, text):
    """
    This function writes text to a file.

    Parameters
    ----------
    filename : str
        The name of the file to write to.
    text : str
        The text to write to the file.

    Returns
    -------
    None
    """
    with open(filename, 'w') as file:
        file.write(text)

def decode(img_path):
    img = np.array(keras.preprocessing.image.load_img(
        path = img_path,
        grayscale=False, 
        color_mode="rgb"))
    return np.expand_dims(img/ 255, axis=0)

def get_labels(generator):
    target_names = []

    for key in generator.class_indices:
        target_names.append(key)
        
    return target_names