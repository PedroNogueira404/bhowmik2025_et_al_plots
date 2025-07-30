"""
This class provides the paths to various directories used in the bhowmik2025
plots project and is imported in the utils module as paths
"""

import os
import logging


class PathUtils:
    """
    Utility class for handling file paths.
    """

    def __init__(self, root=None):
        self.root = os.path.abspath(root) if root else os.path.abspath(".")
        self.input_dir = os.path.join(self.root, "input_files")
        self.fits_dir = os.path.join(self.input_dir, "fits_files")
        self.radial_prof_dir = os.path.join(self.input_dir, "frank_profiles")
        self.output_dir = os.path.join(self.root, "outputs")
        self.latex_dir = os.path.join(self.output_dir, "generated_figures_for_tex")

    def __str__(self):
        return (
            f"PathUtils(root={self.root})\n"
            + f"Input Directory: {self.input_dir}\n"
            + f"FITS Directory: {self.fits_dir}\n"
            + f"Radial Profile Directory: {self.radial_prof_dir}\n"
            + f"Output Directory: {self.output_dir}\n"
            + f"LaTeX Directory: {self.latex_dir}"
        )

    def __repr__(self):
        return self.__str__()

    def log_paths(self):
        """
        path logger
        """
        logging.info("The paths are defined as: \n%s\n%s", self, "#" * 50)
