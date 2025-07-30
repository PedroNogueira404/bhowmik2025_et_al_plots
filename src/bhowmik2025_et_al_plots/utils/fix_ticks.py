import numpy as np
from .arc_to_au import arc_to_au


class FixTicks:
    """
    Class to choose a good number of ticks of an axis, centering it in zero to
    show it as -n_ticks < 0 < n_ticks.
    It uses the box size in units you defined and round it up to force 0
    and integers to appear.
    """

    def __init__(self, max_value=None, ax0=None, ax1=None):
        self.max_value = max_value
        self.ax0 = ax0
        self.ax1 = ax1

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

    def modify_ticks_and_labels_to_au(self, dist, pix_scale, cen_ra_pix, cen_dec_pix):
        """
        Returns both x and y tick positions (in pixels) and corresponding AU labels.
        Only computes shared quantities once.
        """
        delim = FixTicks(max_value=self.max_value)
        arcsec_to_au = arc_to_au(dist)

        label_ticks_au = delim.get_symmetric_ticks_with_zero().astype(int)
        label_ticks_arcsec = label_ticks_au / arcsec_to_au

        pos_xticks_pix = list(label_ticks_arcsec / pix_scale + cen_ra_pix)
        pos_yticks_pix = list(label_ticks_arcsec / pix_scale + cen_dec_pix)

        label_ticks_x = label_ticks_au.astype(str)
        label_ticks_x[0] = ""

        label_ticks_y = label_ticks_au.astype(str)

        return (pos_xticks_pix, label_ticks_x), (pos_yticks_pix, label_ticks_y)

    def set_myticks(self, dist, pix_scale, cen_ra_pix, cen_dec_pix):
        """
        Sets x and y ticks and labels for both ax0 and ax1 using AU units.
        Use it with caution and for individual plots
        """
        (xticks, xlabels), (yticks, ylabels) = self.modify_ticks_and_labels_to_au(
            dist=dist,
            pix_scale=pix_scale,
            cen_ra_pix=cen_ra_pix,
            cen_dec_pix=cen_dec_pix,
        )

        self.ax0.set_xticks(xticks)
        self.ax0.set_xticklabels(xlabels, fontweight="bold")
        self.ax0.set_yticks(yticks)
        self.ax0.set_yticklabels(ylabels, fontweight="bold")
        self.ax0.tick_params(
            axis="both",
            direction="in",
            length=10,
            width=1.5,
            top=True,
            right=True,
            labelsize=14,
        )

    def normalize_ticks_positions(self):
        """
        Normalize the tick positions of ax0 to match ax1's limits.

        Parameters
        ----------
        ax0 : matplotlib.axes.Axes
            The axis with the original ticks.
        ax1 : matplotlib.axes.Axes
            The axis with the target limits.
        """
        # normalized_tick = target_min + (data_tick - data_xlim[0]) * (target_max - target_min) / (data_xlim[1] - data_xlim[0])
        # If the target don't start on 0, we need to adjust the normalization by adding the offset and
        # multiplying by the range
        # ax0 = self.ax0
        # ax1 = self.ax1
        xlim0 = self.ax0.get_xlim()
        xlim1 = self.ax1.get_xlim()

        ylim0 = self.ax0.get_ylim()
        ylim1 = self.ax1.get_ylim()

        # Normalize x ticks
        xticks = self.ax0.get_xticks()

        normalized_xticks = (xticks - xlim0[0]) / (xlim0[1] - xlim0[0]) * (
            xlim1[1] - xlim1[0]
        ) + xlim1[0]

        # Normalize y ticks
        yticks = self.ax0.get_yticks()
        normalized_yticks = (yticks - ylim0[0]) / (ylim0[1] - ylim0[0]) * (
            ylim1[1] - ylim1[0]
        ) + ylim1[0]

        return normalized_xticks, normalized_yticks

    def set_adapted_ticks(self):
        """_summary_
        Instance used only for setting ticks and labels
        for the image ax which have copied other ax
        """
        (xticks, yticks) = self.normalize_ticks_positions()

        self.ax1.set_xticks(xticks)
        self.ax1.set_xticklabels(self.ax0.get_xticklabels(), fontweight="bold")
        self.ax1.set_yticks(yticks)
        self.ax1.set_yticklabels(self.ax0.get_yticklabels(), fontweight="bold")
        self.ax1.tick_params(
            axis="both",
            direction="in",
            length=10,
            width=1.5,
            top=True,
            right=True,
            labelsize=14,
        )
