import numpy as np


def get_symmetric_ticks_with_zero(max_value, tick_spacing):
    """
    Uses the box size in units you defined and round it up to force 0 and integers
    to appear

    Args:
        max_value (float): size in units defined by the user
        tick_spacing (int): The spacing between ticks, in same units

    Returns:
        ticks (list): the ticks to be used as labels (not positions!)
    """
    # Garante que zero sempre esteja presente
    n_ticks = int(np.ceil((max_value / 2 / tick_spacing)))
    ticks = np.arange(-n_ticks, n_ticks + 1) * tick_spacing
    return ticks
