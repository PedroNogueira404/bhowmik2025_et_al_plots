"""
Purpose: Small function to convert from arcsec to au given distance in parsecs
"""

import numpy as np


def arc_to_au(distance_pc):
    """
    Purpose: Small function to convert from arcsec to au given distance in parsecs
    """
    au = (np.pi / (180 * 3600)) * distance_pc * 206265
    return au
