import numpy as np


class FixTicks:
    """
    Class to choose a good number of ticks of an axis, centering it in zero to
    show it as -n_ticks < 0 < n_ticks.
    It uses the box size in units you defined and round it up to force 0
    and integers to appear.
    """

    def __init__(self, max_value):
        self.max_value = max_value

    def choose_tick_spacing(self):
        """
        Choose the largest tick spacing from 'preferred' that gives
        ~4-6 ticks total (2-3 on each side of zero).
        """
        preferred = np.arange(
            5, self.max_value / 2, 5
        )  # [5, 10, 15, 20, 25, 50, 100,150,200]
        for spacing in preferred:
            if (self.max_value) / spacing <= 6:
                return spacing
        return preferred[-1]  # fallback if none fit

    def get_symmetric_ticks_with_zero(self):
        """
        Uses the box size in units you defined and round it up to force 0 and integers
        to appear

        Args:
            max_value (float): size in units defined by the user
            tick_spacing (int): The spacing between ticks, in same units

        Returns:
            ticks (list): the ticks to be used as labels (not positions!)
        """

        tick_spacing = self.choose_tick_spacing()
        n_ticks = int(np.ceil((self.max_value / 2 / tick_spacing)))
        ticks = np.arange(-n_ticks, n_ticks + 1) * tick_spacing
        return ticks
