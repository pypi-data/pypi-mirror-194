import MDAnalysis as mda
import os

class LoadTrajectories:
    def get_files(self, path):
        """
        Returns a dictionary that maps subfolder names to lists of full file paths in those subfolders.
        
        The function looks for subfolders in the input path, and for each subfolder, it creates
        a list of the full file paths for the files in the subfolder that have the '.pdb' or '.xtc'
        extensions. The subfolder name is used as the key in the output dictionary, and the list of
        file paths is used as the value.
        
        Parameters
        ----------
        path : str
            The directory path to search for subfolders.
        
        Returns
        -------
        path_dict : dict
            A dictionary that maps subfolder names to lists of full file paths in those subfolders.
        """
        # Initialize an empty dictionary to store the file lists
        path_dict = {}
        
        # Iterate over the entries in the input path
        for entry in os.listdir(path):
            # Get the full path to the entry
            entry_path = os.path.join(path, entry)
            # If the entry is a directory, process it
            if os.path.isdir(entry_path):
                # Create a list of the full file paths for the files in the subfolder
                # that have the '.pdb' or '.xtc' extensions
                file_paths = [
                    os.path.join(entry_path, file)
                    for file in os.listdir(entry_path)
                    if file.endswith(('.pdb', '.xtc'))
                ]
                # Add the subfolder name and file list to the output dictionary
                path_dict[entry] = file_paths
        
        # Return the output dictionary

        return path_dict
    
    def traj_from_dir(self, path):
        """
        Returns a dictionary that maps subfolder names to trajectories created from the '.pdb' and '.xtc'
        files in those subfolders.
        
        The function uses the `get_files` method to find the '.pdb' and '.xtc' files in the subfolders
        of the input path, and it creates a `Trajectory` object for each pair of '.pdb' and '.xtc' files.
        The subfolder name is used as the key in the output dictionary, and the `Trajectory` object is
        used as the value.
        
        Parameters
        ----------
        path : str
            The directory path to search for subfolders.
        
        Returns
        -------
        traj_dict : dict
            A dictionary that maps subfolder names to trajectories created from the '.pdb' and '.xtc'
            files in those subfolders.
        """
        traj_dict = {}
        # Create the traj_dict dictionary using a dictionary comprehension
        for folder, files_paths in self.get_files(path).items():
            for file_path in files_paths:
                if file_path.endswith('.xtc'):
                       xtc = file_path
                elif file_path.endswith('.pdb'):
                       pdb = file_path
            traj_dict[folder] = mda.Universe(pdb, xtc)


        # Print a message indicating the number of trajectories found
        print(f'Found {len(traj_dict.keys())} trajectories:')
        # print(traj_dict)
        return traj_dict

if __name__ == '__main__':
    pass
