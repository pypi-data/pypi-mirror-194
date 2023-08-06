# Importing libraries
import numpy as np

class Allign:
    """
    A class for aligning and centering a trajectory.
    """

    def __init__(self, ref):
        """
        Initialize the class with a reference frame.

        Parameters
        ----------
        ref : numpy.ndarray
            A 3D NumPy array containing the coordinates of the atoms in the reference frame.
        """
        # Rotate the reference frame using the eigenvectors of ref.T @ ref
        self.ref = ref @ np.linalg.eigh(ref.T @ ref)[1][:, ::-1]


    def transform(self, trj):
        """
        Align and center a given trajectory.

        Parameters
        ----------
        trj : numpy.ndarray
            A 3D NumPy array containing the coordinates of the atoms in the trajectory.

        Returns
        -------
        numpy.ndarray
            A 3D NumPy array containing the aligned and centered coordinates
             of the atoms in the trajectory.
        """
        # Center the  trajectory
        trj = self.center(trj)
        # Align the trajectory to the reference frame
        trj = self.fit(trj)


        return trj

    def fit(self, trj):
        """
        Align a given trajectory to the reference frame.

        Parameters
        ----------
        trj : numpy.ndarray
            A 3D NumPy array containing the coordinates of the atoms in the trajectory.

        Returns
        -------
        numpy.ndarray
            A 3D NumPy array containing the aligned coordinates of the atoms in the trajectory.
        """
        # Use SVD to align the trajectory to the reference frame
        U, L, Vt = np.linalg.svd(self.ref.T @ trj)
        R = U @ Vt

        # Rotate the trajectory using the rotation matrix
        return trj @ R.transpose((0,2,1))

    def center(self, coords):
        """
        Center a given set of coordinates by subtracting the mean of the coordinates for each frame.

        Parameters
        ----------
        coords : numpy.ndarray
            A 3D NumPy array containing the coordinates of the atoms.

        Returns
        -------
        numpy.ndarray
            A 3D NumPy array containing the centered coordinates of the atoms.
        """
        # Calculate the mean of the coordinates for each frame
        # Subtract the mean from the coordinates for each frame

        coords -= coords.mean(axis = 1)[:, None, :]

        return coords


if __name__ == "__main__":
    pass
