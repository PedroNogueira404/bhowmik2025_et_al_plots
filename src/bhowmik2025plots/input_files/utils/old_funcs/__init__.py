"""
This module contains utility functions and constants for the bhowmik2025 plots
project.

It also contains the paths to various directories used in the project.
"""

import os

from .add_beam import add_beam
from .add_sizebar import add_sizebar
from .arc_to_au import arc_to_au
from .fix_ticks import FixTicks

# from .choose_tick_spacing import choose_tick_spacing
# from .get_symmetric_ticks_with_zero import get_symmetric_ticks_with_zero
from .plot_utils import PlotUtils
from .paths import PathUtils

paths = PathUtils()
# input_dir: str = "input_files"
# fits_dir: str = "fits_files"
# radial_prof_dir: str = "frank_profiles"
# output_dir: str = "outputs"
# latex_dir: str = "generated_figures_for_tex"

# ROOT_PROJECT: str = os.path.abspath(".")
# INPUT_DIR: str = f"{ROOT_PROJECT}/{input_dir}"
# OUTPUT_DIR: str = f"{ROOT_PROJECT}/output_dir"
# FITS_DIR: str = f"{INPUT_DIR}/{fits_dir}"
# RADIAL_PROF_DIR: str = f"{INPUT_DIR}/{radial_prof_dir}"
# LATEX_FILES_DIR: str = f"{ROOT_PROJECT}/{latex_dir}"

if __name__ == "__main__":
    print(
        "You are importing variables and modules from: ",
        ROOT_PROJECT + "/" + __package__,
    )
