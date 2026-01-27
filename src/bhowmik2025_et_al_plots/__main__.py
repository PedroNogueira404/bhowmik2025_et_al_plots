"""
Main function - It rewrites all the tables, + files you have chosen to plot
with the configuration you set, + creates the LaTeX text for the images to be plotted
on a grid of 2 columns + logs all necessary info into my_logs.log
"""

import shutil
import os
import logging

from bhowmik2025_et_al_plots import table_creator
from bhowmik2025_et_al_plots import plotter_w_decorators
from bhowmik2025_et_al_plots import images_latex

from bhowmik2025_et_al_plots.utils import PathUtils

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

terminal_formatter = logging.Formatter(
    fmt="[{asctime}]: {message}" + "\n" + 50 * "#",
    style="{",
    datefmt="%H:%M:%S",
)

file_formatter = logging.Formatter(
    fmt="[{levelname} {asctime}]: {message} [(l:{lineno}) [{filename}]]"
    + "\n"
    + 50 * "#",
    style="{",
    datefmt="%H:%M:%S",
)

terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(terminal_formatter)
terminal_handler.setLevel(logging.INFO)
logger.addHandler(terminal_handler)

file_handler = logging.FileHandler("my_logs.log", mode="w", encoding="utf-8")
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)


# logging.basicConfig(
#     filename="my_logs.log",
#     encoding="utf-8",
#     format="%(levelname)s %(asctime)s: %(message)s (l: %(lineno)d) [%(filename)s])",
#     level=logging.INFO,
#     filemode="w",
# )

paths = PathUtils()


def main(reverse: bool = True) -> None:
    """
    Main function calling all core steps of the pipeline.
    """
    paths.log_paths()
    table_creator.creating_tables(verbose=False)

    # if flush:
    #     logging.warning("Flush mode enabled. Deleting content in %s", paths.output_dir)
    flush = (
        input(
            "⚠️  Type 'y' or 'yes' to delete all folders inside 'outputs'. Anything else will cancel:\n"
        )
        .strip()
        .lower()
    )
    if flush in ["y", "yes"]:
        logger.warning("Flush mode enabled. Deleting content in %s", paths.output_dir)
        for name in os.listdir(paths.output_dir):
            full_path = os.path.join(paths.output_dir, name)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
                # print("\nDeleted folder: %s", full_path)
                logger.info("Deleted folder: %s", full_path)
    else:
        # print("Flush aborted by user. No folders deleted.")
        # print(50 * "#")
        logger.info("Flush aborted by user. No folders deleted.")
        # print(50 * "#")
    # singlecolumn = (
    #     input(
    #         "⚠️  Type 'y' or 'yes' use single collumn format on your grids. Anything else will cancel:\n"
    #     )
    #     .strip()
    #     .lower()
    # )
    # if singlecolumn in ["y", "yes"]:
    #     doublecol = False
    #     logger.info("Single column format enabled for LaTeX grids.")
    # else:
    #     doublecol = True
    #     logger.info("Double column format enabled for LaTeX grids.")

    cfg = plotter_w_decorators.load_variables(
        verbose=False,
        _zoom_factor=1,
        smooth=False,
        flux_ordered=None,
        dpi_png=100,
        dpi_pdf=600,
        data_rad=True,
    )

    plotter_w_decorators.plotter(cfg)

    if cfg.flux_ordered:
        reverse = True
    cfg_latex = images_latex.load_variables_grid(reverse=reverse)

    images_latex.generate_all_latex_figures(cfg=cfg_latex)


if __name__ == "__main__":
    # print(50 * "#")
    logger.info("You are rewriting tables and outputs by running the main function.")
    # print(50 * "#")
    main(reverse=True)
