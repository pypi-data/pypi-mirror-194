from MDAnalysis.analysis.base import AnalysisFromFunction
import numpy as np

from Allign import Allign
class ParseTrajectory:
    """
    A class for parsing and analyzing molecular dynamics trajectories using MDAnalysis.

    Attributes:
        no (int): Keeps track of the number of instances of the class.
        ref (ndarray): Reference coordinates used for alignment.
    """
    no  = 0 
    ref = np.array([])

    def __init__(self, name, universe):
        """
        The constructor for the ParseTrajectories class.

        Args:
            name (str): The name of the instance.
            universe (MDAnalysis.core.groups.Universe): The universe object containing the trajectory data.
        """
        self. name = name
        self.universe = universe

        # Increment the class variable 'no' to keep track of the number of instances
        ParseTrajectory.no += 1

        # If this is the first instance, set the reference coordinates
        if ParseTrajectory.no == 1:
            ParseTrajectory.ref = universe.atoms.positions
        
    def get_coords(self):
        """
        Returns the coordinates of the atoms in the trajectory.

        Returns:
            coords (ndarray): The coordinates of the atoms in the trajectory.
        """
        # Use an AnalysisFromFunction to get the coordinates at each frame
        coords = AnalysisFromFunction(lambda ag: ag.positions.copy(), self.universe).run().results
        return coords['timeseries']
    
    def allign(self):
        """
        Aligns the trajectory to the reference coordinates.

        Returns:
            aligned_coords (ndarray): The aligned coordinates of the atoms in the trajectory.
        """
        # Use the Allign class to align the coordinates to the reference coordinates
        return Allign(ParseTrajectory.ref).transform(self.get_coords())

    def __repr__(self):
            """
            Returns a string representation of the class.

            Returns:
                representation (str): A string representation of the class.
            """
            return f'{self.__class__.__name__}(name={self.name}, universe={self.universe.atoms.positions.shape})'

