"""
This module provides a function to add a size bar in AU to a matplotlib axis.
It calculates the size in astronomical units based on the provided arcseconds,
but it wasn't used on the final plots, since their labels were already in AU.
"""

from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

# import numpy as np
import matplotlib.font_manager as fm

from .arc_to_au import arc_to_au


def add_sizebar(
    ax, size_arcsec: float, distance_pc: float, pixscale_arcsec_per_pix: float
):
    """
    Add a size bar to a matplotlib axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to add the size bar to.
    size_arcsec : float
        The size of the bar in arcseconds.
    distance_pc : float
        Distance to the source in parsecs.
    pixscale_arcsec_per_pix : float
        Pixel scale in arcseconds per pixel.
    """

    fontprops = fm.FontProperties(size=16)
    # pixscale is how many arcsecs are in 1 pixel
    # size is in arcsec
    # formula is: parallax_rad = size_pc/distance_pc

    # d_tosource = distance_pc #pc
    # d_tosource = d_tosource*206265 #au
    # arc2rad = numpy.pi/(180*3600)
    # size_rad = size_arcsec*arc2rad
    size_au = size_arcsec * arc_to_au(distance_pc)
    # "{:.0f}".format(size_rad*d_tosource)+' au',
    # transform=ax.get_transform('pixel')
    asb = AnchoredSizeBar(
        ax.transData,
        size_arcsec / pixscale_arcsec_per_pix,
        "{:.0f}".format(size_au) + " au",
        loc=4,
        fontproperties=fontprops,
        pad=0.1,
        borderpad=0.5,
        sep=5,
        size_vertical=0.2,
        color="black",
        frameon=False,
    )

    ax.add_artist(asb)
