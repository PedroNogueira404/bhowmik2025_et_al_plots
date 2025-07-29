import numpy as np


def choose_tick_spacing(max_value):
    """
    Choose the largest tick spacing from 'preferred' that gives ~4-6 ticks total
    (2-3 on each side of zero).
    """
    preferred = np.arange(5, max_value / 2, 5)  # [5, 10, 15, 20, 25, 50, 100,150,200]
    for spacing in preferred:
        if (max_value) / spacing <= 6:
            return spacing
    return preferred[-1]  # fallback if none fit
