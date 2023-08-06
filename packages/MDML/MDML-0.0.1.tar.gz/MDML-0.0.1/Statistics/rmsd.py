import numpy as np

class RMSD: 
    """ 
    ----------
    coords : numpy array
        The initial set of coordinates to compare against.


    Attributes
    ----------
    coords : numpy array
        The initial set of coordinates to compare against.

    """
    def __init__(self, coords):
        """
        Initialize the class with the input coordinates.
        """
        self.coords = coords

    def _similarity(self, A, B):
        """
        Private method to calculate the similarity between two sets of coordinates.

    

        Parameters
        ----------
        A : numpy array
            First set of coordinates to compare.
        B : numpy array
            Second set of coordinates to compare.

    

        Returns
        -------
        similarity : float
            The similarity between the two sets of coordinates.
        """
        return np.linalg.svd(A.T @ B, compute_uv=False).sum(axis=1) / len(A)

    

    def compute_avg_structure(self):
        """
        Returns the average structure of the last 10% of the frames.

    

        Returns
        -------
        avg_structure : numpy array
            The average structure of the last 10% of the frames.
        """
        return self.coords[-(len(self.coords)//10):].mean(axis=0)

    

    def compute_rgyr2_mean(self):
        """
        Returns the mean radius of gyration squared of the average structure.

    

        Returns
        -------
        rgyr2_mean : float
            The mean radius of gyration squared of the average structure.
        """
        avg_structure = self.compute_avg_structure()
        rgyr2_mean = (avg_structure ** 2).sum() / len(avg_structure)
        return rgyr2_mean

    

    def compute_rgyr2(self, coords):
        """
        Returns the radius of gyration squared of the input coordinates.

    

        Parameters
        ----------
        coords : numpy array
            The set of coordinates to calculate the radius of gyration squared for.

    

        Returns
        -------
        rgyr2 : float
            The radius of gyration squared of the input coordinates.
        """
        rgyr2 = (coords ** 2).sum(axis=(1, 2)) / coords.shape[1]
        return rgyr2

    

    def calculate_rmsd(self, against = None):
        """
        Returns the RMSD between the initial coordinates and the input coordinates or the average structure if no input is provided.

        
        Parameters
        ----------
        against : numpy array, optional
            The set of coordinates to compare against, if not provided the average structure is used.

    

        Returns
        -------
        rmsd : float
            The root mean square deviation between the initial coordinates and the input coordinates or the average structure.
        """
        if against is not None:
            rgyr2 = self.compute_rgyr2(against)
            similarity = self._similarity(self.compute_avg_structure(), against)
        else:
            rgyr2 = self.compute_rgyr2(self.coords)
            similarity = self._similarity(A = self.compute_avg_structure(),
                                        B = self.coords)
        return (self.compute_rgyr2_mean() + rgyr2 - 2 * similarity) ** 0.5
    
if __name__ == '__main__':
    pass
