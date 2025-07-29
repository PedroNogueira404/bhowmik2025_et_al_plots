import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm

class PlotUtils:
    def __init__(self):
        self.positions = {
            'title': (0.25, 0.93),
            'flux': (0.7, 0.13)
        }
        self.colors = {
            'beam_edge': 'red',
            'beam_face': 'white',
            'sizebar': 'black',
            'sizebar_text': 'black'
        }
        self.n_axes = 3
        self.fontprops = fm.FontProperties(size=16)
        self.tick_labelsize = 14

    @staticmethod
    def arc_to_au(distance_pc):
        return (np.pi/(180*3600))*distance_pc*206265

    def add_sizebar(self, ax, size_arcsec, distance_pc, pixscale_arcsec_per_pix):
        size_au = size_arcsec * self.arc_to_au(distance_pc)
        asb = AnchoredSizeBar(
            ax.transData,
            size_arcsec/pixscale_arcsec_per_pix,
            "{:.0f}".format(size_au) + ' au',
            loc=4,
            fontproperties=self.fontprops,
            pad=0.1, borderpad=0.5, sep=5, size_vertical=0.2,
            color=self.colors['sizebar'], frameon=False)
        ax.add_artist(asb)

    def add_beam(self, ax, bmaj, bmin, bpa, pixscale_arcsec_per_pix,
                 offset_fraction_x=0.15, offset_fraction_y=0.15):
        bmaj_pix = bmaj / pixscale_arcsec_per_pix
        bmin_pix = bmin / pixscale_arcsec_per_pix
        bpa = bpa + 90
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        offset_x = xlim[0] + offset_fraction_x * (xlim[1] - xlim[0])
        offset_y = ylim[0] + offset_fraction_y * (ylim[1] - ylim[0])
        ellipse = mpatches.Ellipse(
            (offset_x, offset_y),
            width=bmaj_pix,
            height=bmin_pix,
            angle=bpa,
            edgecolor=self.colors['beam_edge'],
            facecolor=self.colors['beam_face'],
            alpha=1,
            linestyle='solid',
            lw=1.5)
        ax.add_patch(ellipse)

    @staticmethod
    def normalize_ticks_positions(ax1, ax2):
        xlim1 = ax1.get_xlim()
        xlim2 = ax2.get_xlim()
        ylim1 = ax1.get_ylim()
        ylim2 = ax2.get_ylim()
        xticks = ax1.get_xticks()
        normalized_xticks = (xticks - xlim1[0]) / (xlim1[1] - xlim1[0]) * (xlim2[1] - xlim2[0]) + xlim2[0]
        yticks = ax1.get_yticks()
        normalized_yticks = (yticks - ylim1[0]) / (ylim1[1] - ylim1[0]) * (ylim2[1] - ylim2[0]) + ylim2[0]
        return normalized_xticks, normalized_yticks

    @staticmethod
    def choose_tick_spacing(max_value, preferred=[5, 10, 15, 20, 25, 50, 100]):
        for spacing in preferred:
            if (2 * max_value) / spacing <= 6:
                return spacing
        return preferred[-1]

    @staticmethod
    def get_symmetric_ticks_with_zero(max_value, tick_spacing):
        n_ticks = int(np.ceil(max_value / tick_spacing))
        ticks = np.arange(-n_ticks, n_ticks + 1) * tick_spacing
        return ticks

    def set_tick_labels_bold(self, ax):
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')
        ax.tick_params(axis='both', labelsize=self.tick_labelsize)

    def set_box_aspect(self, ax, aspect=1):
        ax.set_box_aspect(aspect)