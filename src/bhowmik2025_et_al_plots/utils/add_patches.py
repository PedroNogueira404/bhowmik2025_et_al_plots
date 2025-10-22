# import matplotlib.patches as mpatches
# import matplotlib.font_manager as fm

# from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# import matplotlib.pyplot as plt

# from .arc_to_au import arc_to_au


class AddPatches:
    """
    Class to encapsulate all the patches of the figures such as texts, sizebars and beam.
    """

    def __init__(self, ax) -> None:
        self.ax = ax

    def add_beam(
        self,
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
        import matplotlib.patches as mpatches

        # Convert bmaj/bmin from arcsec to pixels
        bmaj_pix = bmaj / pixscale_arcsec_per_pix
        bmin_pix = bmin / pixscale_arcsec_per_pix
        bpa = bpa + 90

        # Get axis limits in pixels
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

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

        return self.ax.add_patch(ellipse1)

    def add_sizebar(
        self, size_arcsec: float, distance_pc: float, pixscale_arcsec_per_pix: float
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
        import matplotlib.font_manager as fm
        from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
        from .arc_to_au import arc_to_au

        fontprops = fm.FontProperties(size=16)
        # pixscale is how many arcsecs are in 1 pixel
        # formula is: parallax_rad = size_pc/distance_pc
        # d_tosource = distance_pc #pc
        # d_tosource = d_tosource*206265 #au
        # arc2rad = numpy.pi/(180*3600)
        # size_rad = size_arcsec*arc2rad
        size_au = size_arcsec * arc_to_au(distance_pc)
        asb = AnchoredSizeBar(
            self.ax.transData,
            size_arcsec / pixscale_arcsec_per_pix,
            label=f"{size_au:.0f}" + " au",
            loc=4,
            fontproperties=fontprops,
            pad=0.1,
            borderpad=0.5,
            sep=5,
            size_vertical=0.2,
            color="black",
            frameon=False,
        )

        return self.ax.add_artist(asb)

    def add_name_text(self, name=None) -> None:
        """_summary_"""
        return self.ax.text(
            0.27,
            0.93,
            name.replace("_", " ").upper(),
            transform=self.ax.transAxes,
            fontsize=16,
            ha="center",
            va="top",
            color="black",
            fontweight="bold",
            bbox=dict(
                facecolor="white",
                edgecolor="red",
                boxstyle="round,pad=0.2",
                alpha=0.9,
            ),
        )

    def add_flux_text(self, flux=None) -> None:
        """_summary_"""
        return self.ax.text(
            0.78,
            0.11,
            s=f"{flux:.2f} mJy",
            transform=self.ax.transAxes,
            fontsize=16,
            ha="center",
            va="top",
            color="black",
            fontweight="bold",
            bbox=dict(
                facecolor="white",
                edgecolor="red",
                boxstyle="round,pad=0.2",
                alpha=0.9,
            ),
        )

    def add_colorbar(
        self, fig=None, im=None, pos="top", orientation="horizontal"
    ) -> None:
        """
        Add_colorbar

        """
        import matplotlib.pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        ax = self.ax
        divider = make_axes_locatable(ax)
        cax = divider.append_axes(pos, size="3%", pad=0)
        cbar = fig.colorbar(im, cax, orientation=orientation)
        cbar.ax.xaxis.set_label_position(pos)
        cbar.ax.xaxis.set_ticks_position(pos)

        def format_func(x, pos):
            """
            Format ticks: multiply by 1000 and show as integer
            """
            return f"{x*1000:.1f}"

        cbar.ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
        cbar.ax.tick_params(labelsize=14)  # Tick label size
        for label in cbar.ax.get_xticklabels():
            label.set_fontweight("bold")
