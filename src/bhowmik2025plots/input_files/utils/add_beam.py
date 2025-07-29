"""Function to add a beam ellipse to a matplotlib axis."""

import matplotlib.patches as mpatches


def add_beam(
    ax,
    bmaj: float,
    bmin: float,
    bpa: float,
    pixscale_arcsec_per_pix: float,
    offset_fraction_x: float = 0.15,
    offset_fraction_y: float = 0.15,
):
    """
    Add a beam ellipse to the image, placed in the lower-left corner.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to add the beam to.
    bmaj : float
        Beam major axis (arcsec).
    bmin : float
        Beam minor axis (arcsec).
    bpa : float
        Beam position angle (degrees).
    pixscale_arcsec_per_pix : float
        Arcsec per pixel.
    offset_fraction_x, offset_fraction_y : float
        Fractions (0-1) of the axis size to offset the beam center from the corner.
    """

    # Convert bmaj/bmin from arcsec to pixels
    bmaj_pix = bmaj / pixscale_arcsec_per_pix
    bmin_pix = bmin / pixscale_arcsec_per_pix
    bpa = bpa + 90

    # Get axis limits in pixels
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Define position for the beam (bottom-left with offset)
    offset_x = xlim[0] + offset_fraction_x * (xlim[1] - xlim[0])
    offset_y = ylim[0] + offset_fraction_y * (ylim[1] - ylim[0])

    ellipse1 = mpatches.Ellipse(
        (offset_x, offset_y),  # (x, y) center in pixels
        width=bmaj_pix,  # total width (major axis)
        height=bmin_pix,  # total height (minor axis)
        angle=bpa,  # rotation angle in degrees
        edgecolor="red",
        facecolor="white",
        alpha=1,
        linestyle="solid",
        lw=1.5,
    )

    ax.add_patch(ellipse1)
