def rmsf(coords):
    """
    Returns the RMSF of the initial coordinates.        

    Returns
    -------
    rmsf : list
        The root mean square flactuation of the initial coordinates 

    """
    coords -= coords.mean(axis = 0)
    return ((coords**2).mean(axis = 0 )** 0.5).mean(axis = 1)