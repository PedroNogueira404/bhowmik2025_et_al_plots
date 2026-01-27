"""
Functions to make all the plots based on the input collumns of full_table,
created with table_creator.py, feature labels given by gap_ring_infl_pt.csv and
frank_profiles
"""

# === Standard Library ===
from functools import wraps
import os
import time
import warnings
import logging

# import sys
from dataclasses import dataclass


# === Third-Party ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# from scipy import special
from tqdm import tqdm
from scipy.ndimage import gaussian_filter
from astropy.io import fits
from astropy.wcs import WCS
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.utils.exceptions import AstropyWarning

# === Internal ===

from bhowmik2025_et_al_plots.utils import (
    AddPatches,
    arc_to_au,
    FixTicks as ft,
    PathUtils,
)

warnings.simplefilter("ignore", category=AstropyWarning)
################################################################################

paths = PathUtils()
# logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


@dataclass
class PlotConfig:
    """Store variable names and types to be called as configs by load_variables
    and set as cfg parameters in plotter()
    """

    features_data: pd.DataFrame
    subset: pd.DataFrame
    index_to_groups: dict
    im_type: str
    verbose: bool
    flux_ordered: bool
    smooth: bool
    special_cases: dict
    zoom_factor: int
    first_file: int
    last_file: int
    delimiter: int
    dpi: int
    data_res: bool


def load_variables(
    verbose: bool = False,
    smooth: bool = False,
    _zoom_factor: int = 1,
    flux_ordered: bool = None,
    dpi_pdf: int = 600,
    dpi_png: int = 100,
    data_res: bool = True,
) -> dict:
    """Function to load all the variables to be used in the main plotter() function"""
    csv_features: str = (
        f"{paths.input_dir}/gap_ring_infl_pt.csv"  # <-- Your annotated features file
    )
    features_data = pd.read_csv(csv_features, index_col=False)
    features_data["Target"] = features_data["Target"].astype(str).str.lower()
    full_table = pd.read_csv(f"{paths.input_dir}/full_table.csv", index_col=False)

    index_to_groups = full_table.groupby(by="id")["Group"].apply(func=list).to_dict()
    ################################################################################
    # Ask user if they want to proceed with flux-ordered (PDF) output
    proceed = (
        input(
            "\nDo you want to proceed with flux-ordered output as PDF files? [Y/n] (blank=True):\n"
        )
        .strip()
        .lower()
    )
    # Reevaluate flux_ordered i.e. if the images will be saved as pngs or pdfs by the user
    if proceed in ["", "y", "yes"]:
        flux_ordered = True
    else:
        flux_ordered = False

    # Now set parameters based on the user's choice
    if flux_ordered:
        _im_type = "pdf"
        full_table = full_table.sort_values("B8_Flux")
        dpi = dpi_pdf
    else:
        _im_type = "png"
        dpi = dpi_png

    logger.info(
        "flux_ordered was set to %s, and files will be saved as %s with %s dpi",
        flux_ordered,
        _im_type,
        dpi,
    )

    first_file_input = input("\n Start index (blank = 0): ")
    last_file_input = input("End index (blank or 'None' = no end):")

    first_file = (
        int(first_file_input)
        if first_file_input.strip().lower() not in ("", "none")
        else 0
    )

    last_file = (
        int(last_file_input)
        if last_file_input.strip().lower() not in ("", "none")
        else len(full_table)
    )
    logger.info("You have chosen  [ %d - %d ] range of files", first_file, last_file)
    ################################################################################
    ### Change if you want to limit the number of files sequentially processed
    delimiter: int = 101
    ################################################################################

    subset = full_table[first_file:last_file]
    ####################################################################
    # adding SPECIAL CASES
    sc_newvmin = ["odisea_c4_41", "odisea_c4_143", "odisea_c4_51"]
    sc_smooth = list(
        full_table[(full_table["Stage"] == 0) | (full_table["Stage"] == 1)]["field"]
    )
    sc_fill_blank_model = ["odisea_c4_094a", "odisea_c4_094b"]
    sc_nomodel = [""]  # ["odisea_c4_094b"]
    special_cases = {
        "smooth": sc_smooth,
        "apply_1%": sc_newvmin,
        "fillmodel": sc_fill_blank_model,
        "nomodel": sc_nomodel,
    }

    ####################################################################

    return PlotConfig(
        features_data=features_data,
        subset=subset,
        index_to_groups=index_to_groups,
        im_type=_im_type,
        verbose=verbose,
        flux_ordered=flux_ordered,
        smooth=smooth,
        zoom_factor=_zoom_factor,
        first_file=first_file,
        last_file=last_file,
        delimiter=delimiter,
        dpi=dpi,
        special_cases=special_cases,
        data_res=data_res,
    )


def time_and_loadbar_decorator(func) -> None:
    """
    Decorator to calculate elapsed time and show progress bar
    """

    @wraps(func)
    def wrapper(cfg):
        initial_time = time.time()
        result = list(tqdm(func(cfg), desc="Processing files", total=len(cfg.subset)))
        end_time = time.time()
        elapsed_time = end_time - initial_time
        minutes = int(elapsed_time // 60)
        secs = f"{elapsed_time % 60:05.2f}"

        logger.info("Elapsed plotting/saving time: %02d:%s", minutes, secs)

        return result

    return wrapper


@time_and_loadbar_decorator
def plotter(cfg: PlotConfig):
    """
    Main plotting function initialized in the for ranging the data and model fits files
    """
    for count, row in enumerate(cfg.subset.itertuples(index=False)):
        if count > cfg.delimiter:
            break

        i = row.path
        j = row.path_model
        profile_file = row.path_rad
        name = row.field
        r_frank = row.Rmax_frank
        cen_x_sex = row.center_x
        cen_y_sex = row.center_y
        bpa = row.beam_pa
        bmaj = row.beam_maj
        bmin = row.beam_min
        dist = row.Distance
        b8_flux = row.B8_Flux
        disk_id = row.id
        isbinary = row.isbinary
        r_zoom = row.R_zoom
        rms_data = row.rms_data
        # rms_model = row.rms_model_profile
        ########### Calculating global variables

        # Reading coords Trisha gave me
        coord = SkyCoord(
            ra=cen_x_sex,
            dec=cen_y_sex,
            unit=(u.hourangle, u.deg),
            frame="fk5",
            equinox="J2000.0",
        )

        ########### Ax2 ######################################################
        # -----------------------------------------------------------------------
        # Function to calculate Rp while preserving rings
        def Rp_au_preserve_rings(r_au, I_profile, p=0.95, eps_rel=0.210):
            """
            r_au: radius array (AU) – increasing
            I_profile: surface-brightness (any units; normalization cancels)
            p: enclosed-flux fraction (0.90 for R90, 0.95 for R95)
            eps_rel: peak threshold to keep 'significant' rings (e.g. 8% of global peak)
            """
            r = np.asarray(r_au, float)
            I = np.asarray(I_profile, float)
            if np.any(np.diff(r) <= 0):
                idx = np.argsort(r)
                r, I = r[idx], I[idx]

            I = np.nan_to_num(I, nan=0.0)
            I[I < 0] = 0.0

            # ---- find last significant local maximum ----
            Imax = I.max()
            if Imax <= 0:
                return np.nan
            # local peaks
            pk_mask = (I[1:-1] > I[:-2]) & (I[1:-1] > I[2:])
            peaks = np.where(pk_mask)[0] + 1
            if peaks.size == 0:
                i_last = int(np.argmax(I))
            else:
                sig = peaks[I[peaks] >= eps_rel * Imax]  # keep peaks ≥ eps_rel * peak
                i_last = int(sig[-1]) if sig.size else int(np.argmax(I))

            # ---- suppress only beyond the last significant peak (keeps real ring) ----
            J = I.copy()
            if i_last + 1 < len(J):
                J[i_last + 1 :] = np.minimum.accumulate(J[i_last + 1 :])

            # ---- enclosed flux with proper annular weight (trapezoid) ----
            ann = 2.0 * np.pi * r * J
            cum = np.concatenate(
                ([0.0], np.cumsum(0.5 * (ann[1:] + ann[:-1]) * np.diff(r)))
            )
            total = cum[-1]
            if total <= 0:
                return np.nan

            return float(np.interp(p * total, cum, r))

        # ----------------------------------------------------------------------
        prof_data = np.loadtxt(profile_file, unpack=True)
        r_arcsec, flxx = prof_data[0], prof_data[1]

        # Normalize the flux
        flux_max = np.nanmax(flxx)
        flxx /= flux_max  # np.nanmax(flxx)
        # thresh_norm_model = rms_model / flux_max
        r_au = r_arcsec * arc_to_au(dist)
        # r_arcsec, flxx, distance_pc already defined
        R90_au = Rp_au_preserve_rings(r_au, flxx, p=0.90)
        R95_au = Rp_au_preserve_rings(r_au, flxx, p=0.95)
        r_max = R95_au
        # cumulative_flux = np.cumsum(flxx)
        # cumulative_flux /= cumulative_flux[-1]

        # r_limit_idx = np.argmax(cumulative_flux >= 0.95)
        # r_max = r_au[r_limit_idx]

        # Filter only the needed rows
        subset_features = cfg.features_data.loc[
            cfg.features_data["Target"] == name
        ].rename(columns={"D/B": "Label", "R": "R_feature_au"})

        ##########################################################################

        with fits.open(i) as hdul_data, fits.open(j) as hdul_model:

            ############ Reading the FITS files ##############
            if cfg.verbose:
                print("\n", 50 * "#")
                # print(f"\n Processing {count}, of source id {disk_id} \n: {i} \n ")
                logger.info(f"Processing {count}, of source id {disk_id}: {i}")

            # count += 1

            # Extracting header and data from the FITS files
            header_data = hdul_data[0].header
            data_data = hdul_data[0].data

            header_model = hdul_model[0].header
            data_model = hdul_model[0].data

        ########################################
        # Loading wcs
        pixel_scale_data: float = header_data["CDELT2"] * 3600  # in arcsec / pixel
        pixel_scale_model = r_frank * 2 / header_model["NAXIS1"]  # in arcsec / pixel
        wcs = WCS(header_data)

        # Defining centers
        center_ra_deg, center_dec_deg = coord.ra.deg, coord.dec.deg
        center_ra_pix, center_dec_pix = wcs.all_world2pix(
            center_ra_deg, center_dec_deg, 0
        )
        ########################################
        # Definying total boxsize and few more parameters
        # In case you want to apply a zoom factor manually

        imsize_radius_model_arcsec: float = r_zoom  # in arcsec
        imsize_model_pix: float = header_model["NAXIS1"]  # in pix
        imsize_radius_data_pix = imsize_radius_model_arcsec / pixel_scale_data  # in pix
        imsize_radius_model_pix = (
            imsize_radius_model_arcsec / pixel_scale_model
        )  # in pix

        boxsize_au = (
            np.round((imsize_radius_model_arcsec * 2) * arc_to_au(dist), -1)
            / cfg.zoom_factor
        )  # Value -1 corresponds to rounding to the nearest 10 au

        ########################################

        fig = plt.figure(figsize=(15, 5), layout="constrained")
        #################### AX0 - DATA #################################################

        ax0 = plt.subplot(131)

        if cfg.smooth or (name in cfg.special_cases["smooth"]):
            # Smooth the disk
            _sigma = 2
            smooth_data = gaussian_filter(data_data, sigma=_sigma, mode="nearest")
            im0 = ax0.imshow(
                X=smooth_data,
                origin="lower",
                cmap="turbo",
                aspect="equal",
                vmin=rms_data,
            )
            # logger.info(15 * "!" + f" {name} was smoothed with gaussian {_sigma}")
            # print(f"{name} was smoothed with gaussian {_sigma}")
        else:
            im0 = ax0.imshow(
                X=data_data,
                origin="lower",
                cmap="turbo",
                aspect="equal",
                vmin=rms_data,
            )
        # Label
        plt.xlabel(r"$\Delta$RA (au)", fontsize=16, fontweight="bold")
        plt.ylabel(r"$\Delta$DEC (au)", fontsize=16, fontweight="bold")

        # Limits
        ax0.set_xlim(
            center_ra_pix - (imsize_radius_data_pix) / cfg.zoom_factor,
            center_ra_pix + (imsize_radius_data_pix) / cfg.zoom_factor,
        )
        ax0.set_ylim(
            center_dec_pix - (imsize_radius_data_pix) / cfg.zoom_factor,
            center_dec_pix + (imsize_radius_data_pix) / cfg.zoom_factor,
        )

        ## Fixing ticks (pix) and labels (au) ###
        ticks_and_labels_ax0 = ft(boxsize_au, ax0=ax0)
        ticks_and_labels_ax0.set_myticks(
            dist, pixel_scale_data, center_ra_pix, center_dec_pix
        )
        ##################################################
        ## Adding patches ###
        patcher_ax0 = AddPatches(ax0)
        patcher_ax0.add_beam(bmaj, bmin, bpa, pixel_scale_data)
        patcher_ax0.add_name_text(name=name)
        patcher_ax0.add_flux_text(flux=b8_flux)
        patcher_ax0.add_colorbar(fig, im0)

        #################### AX1 - MODEL ###################################
        ax1 = plt.subplot(132)
        vmax = np.nanmax(data_model.data)
        if isbinary == 1:
            vmin = 0.1 * vmax
        elif name in cfg.special_cases["apply_1%"]:
            vmin = 0.01 * vmax
            logger.info(f"1% as vmin were applied to {name}")
        else:
            vmin = 0.05 * vmax  # rms_model

        if name in cfg.special_cases["nomodel"]:
            nan_matrix = np.full(data_model.data.shape, np.nan)
            ax1.imshow(nan_matrix)
            ax1.set_xticks([])
            ax1.set_yticks([])
            ax1.set_xticklabels([])
            ax1.set_yticklabels([])
        else:
            ax1.imshow(
                data_model.data,
                origin="lower",
                cmap="turbo",
                aspect="equal",
                vmin=vmin,
            )

            ####################################################
            # Limits
            ax1.set_xlim(
                imsize_model_pix / 2 - (imsize_radius_model_pix) / cfg.zoom_factor,
                imsize_model_pix / 2 + (imsize_radius_model_pix) / cfg.zoom_factor,
            )
            ax1.set_ylim(
                imsize_model_pix / 2 - (imsize_radius_model_pix) / cfg.zoom_factor,
                imsize_model_pix / 2 + (imsize_radius_model_pix) / cfg.zoom_factor,
            )
            ####################################################
            ## Fixing ticks (pix) and labels (au) ###
            adapt_ax1_ticks_labels = ft(ax0=ax0, ax1=ax1)
            adapt_ax1_ticks_labels.set_adapted_ticks()
            ####################################################
            plt.xlabel(r"$\Delta$RA (au)", fontsize=16, fontweight="bold")
            plt.ylabel(r"$\Delta$DEC (au)", fontsize=16, fontweight="bold")
        if (
            name in cfg.special_cases["fillmodel"]
            or name in cfg.special_cases["nomodel"]
        ):
            # print(name)
            ax1.set_facecolor("black")

        #################### AX2 - RADIAL_PROFILE ######################################
        ax2 = plt.subplot(133)
        if name in cfg.special_cases["nomodel"]:
            ax2.plot()
            ax2.set_xticks([])
            ax2.set_yticks([])
            ax2.set_xticklabels([])
            ax2.set_yticklabels([])
            ax2.set_facecolor("black")
        else:

            ax2 = plt.subplot(133)

            ax2.plot(r_au, flxx, "k-", linewidth=2)

            # Iterate through each source features in gap_ring_infl_pt.csv

            # Create a sorted list of labels
            # print(subset_features["Label"].dropna())
            sorted_labels = list(
                subset_features["Label"].sort_values(
                    key=lambda x: x.str.split("-").str[1].astype(int)
                )
            )
            # Loop through the sorted labels, but get the matching R_au from the original DataFrame
            for idx, feature_label in enumerate(sorted_labels):
                row = subset_features[subset_features["Label"] == feature_label]
                r_feature_au = row["R_feature_au"].values[0]

                if feature_label.startswith("D"):
                    color = "b"
                    linestyle = "dotted"
                elif feature_label.startswith("B"):
                    color = "r"
                    linestyle = "dashed"
                elif feature_label.startswith("I"):
                    color = "g"
                    linestyle = "dashdot"
                else:
                    continue  # Skip unknown features

                y_profile = np.interp(r_feature_au, r_au, flxx)
                plt.vlines(
                    r_feature_au,
                    ymin=y_profile,
                    ymax=0.78,
                    color=color,
                    linestyle=linestyle,
                )

                if y_profile < 0.78:
                    y_text = 0.8 + 0.11 * (idx % 2)
                else:
                    y_text = 0.65 * y_profile
                plt.text(
                    r_feature_au,
                    y_text,
                    feature_label,
                    color=color,
                    fontsize=12,
                    ha="center",
                    va="bottom",
                    rotation=90,
                    fontweight="bold",
                )

            ax2.set_xlabel("Radius (au)", fontsize=16, fontweight="bold")
            ax2.set_ylabel("Normalized Intensity", fontsize=16, fontweight="bold")

            # Write tick labels in boldface
            for label in ax2.get_xticklabels() + ax2.get_yticklabels():
                label.set_fontweight("bold")
            plt.minorticks_on()
            plt.xlim(left=0)
            plt.ylim(bottom=0)

            right_limit = plt.gca().get_xlim()[1]

            plt.axvline(r_max, color="black", linestyle=":", lw=2.5, alpha=0.8)
            if isbinary == 1:
                imax = 0.1
                plt.axhspan(0, imax, alpha=0.2, color="red")
                plt.axhline(imax, color="black", linestyle=":", lw=2.5, alpha=0.8)
            elif name in cfg.special_cases["apply_1%"]:
                imax = 0.01
                plt.axhspan(0, imax, alpha=0.2, color="red")
                plt.axhline(imax, color="black", linestyle=":", lw=2.5, alpha=0.8)
            else:
                imax = 0.05
                plt.axhspan(0, imax, alpha=0.2, color="red")
                plt.axhline(imax, color="black", linestyle=":", lw=2.5, alpha=0.8)
            plt.axvspan(r_max, right_limit, alpha=0.2, color="gray", hatch="/")
            ax2.tick_params(axis="both", width=1, top=True, right=True, labelsize=14)

        #######################################################################################
        ax0.set_box_aspect(1)
        ax1.set_box_aspect(1)
        ax2.set_box_aspect(0.99)
        #######################################################################################

        if cfg.flux_ordered:
            image_name = f"{count:03d}_{name}_cutout.pdf"
        else:
            image_name = f"{name}_cutout.png"

        for group in cfg.index_to_groups.get(disk_id, []):
            save_dir = os.path.join(paths.output_dir, cfg.im_type + "/" + group)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, image_name)
            plt.savefig(save_path, bbox_inches="tight", dpi=cfg.dpi)
            if cfg.verbose:
                print(f"Image saved as {image_name} in: \n {save_path}")
                print(50 * "#")

            plt.close()

        yield count


if __name__ == "__main__":
    print(f"Running {__file__.rsplit('/',maxsplit=1)[-1]} directly")
    cfg = load_variables(verbose=False, _zoom_factor=1, smooth=False)
    plotter(cfg)


def main():
    cfg = load_variables(verbose=False, _zoom_factor=1, smooth=False)
    plotter(cfg)
