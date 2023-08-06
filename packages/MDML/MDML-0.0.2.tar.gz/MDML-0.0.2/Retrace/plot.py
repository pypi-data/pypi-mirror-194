import matplotlib.pyplot as plt

def plot_saliencny_map(sal_map, title, path_to_save):
    """
    This function takes in a saliency map and saves the map
    as an image.

    python

    Parameters
    ----------
    sal_map: numpy.ndarray
        A 2D array representing the saliency map
    title: str
        The title for the saliency map
    path_to_save: str
        The path to save the saliency map

    """
    plt.title(title)
    plt.imshow(sal_map, cmap= 'gray')
    plt.clim(0, 1)
    plt.savefig(path_to_save)