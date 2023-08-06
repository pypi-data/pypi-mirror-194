import numpy as np
import tensorflow as tf

def down_sample(trajectory, num_images):
        """
        Extract a specified number of sub-trajectories from a given trajectory.
        
        Parameters
        ----------
        trajectory : numpy.ndarray
            A 3D NumPy array containing the coordinates of the atoms in the trajectory.
        num_images : int
            The number of sub-trajectories to extract from the trajectory.
        
        Returns
        -------
        list of numpy.ndarray
            A list of NumPy arrays, each containing a sub-trajectory of the original trajectory.
        """
        # Calculate the number of frames in the trajectory
        num_frames = trajectory.shape[0]
        
        # Calculate the number of frames that will be excluded from the mini-trajectories
        mod = num_frames % num_images
        
        if mod != 0:
            # Exclude the first 'mod' frames from the trajectory
            trajectory = trajectory[mod:, :]
            print(f'WARNING: Unable to index full trajectory for {num_images} images, excluded first {mod} frames')
        
        # Extract the desired frames from the trajectory using NumPy array indexing and slicing
        mini_trajs = [trajectory[index:num_frames:num_images, :] for index in range(num_images)]
        
        # Return the resulting mini-trajectories as a list of NumPy arrays
        return np.array(mini_trajs)



def xyz2rgb(traj):
    """
    Convert XYZ trajectory to RGB images.
    """
    no_frames = traj.shape[0]
    rgb = [np.array(tf.keras.preprocessing.image.array_to_img(traj[frame]))
           for frame in range(no_frames)]
    return np.array(rgb)