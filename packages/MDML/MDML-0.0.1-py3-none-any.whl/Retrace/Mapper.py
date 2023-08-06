import os

def get_image_paths(path):
    """
    Generates the full path of each `.jpg` file in the specified `path`.

    Parameters:
        path (str): The path to the directory containing the image files.

    Yields:
        str: The full path to each `.jpg` file in the specified `path`.
    """
    for filename in os.scandir(path):
        if filename.is_file() and filename.name.endswith('.jpg'):
            yield filename.path



def find_res_index(state, ca):
    """
    This function takes in a state and a list of indices of
    Calcium atoms and returns a string of residues associated
    with those indices.

    markdown

    Parameters
    ----------
    state: mdtoolkit.universe.Universe
        The state that needs to be processed
    ca: List[int]
        Indices of Calpha atoms

    Returns
    -------
    str
        A string of the important residues separated by comma

    """
    index = 0 
    res_str = ''

    for atom in state.atoms:
        if atom.name == 'CA':
            index += 1
            if index in ca:
                res = str(atom.residue)
                res = res.split(' ')[-1][:-1]
                res_str += res
                res_str += ', '

    return res_str[:-2]

if __name__ == "__main__":
    pass
