import os
import shutil
import logging
import pandas as pd
from dataclasses import dataclass

from bhowmik2025_et_al_plots.utils import PathUtils

logger = logging.getLogger(__name__)
paths = PathUtils()

full_table = pd.read_csv(f"{paths.input_dir}/full_table.csv", index_col=False)

pdf_dir = os.path.join(paths.output_dir, "pdf")
groups = full_table["Group"].unique()


def latex_images(images, doublecol: bool, folder, super_folder="pdf"):
    """
    Generate a LaTeX string for a row of up to 2 images as minipages.
    Args:
        images (list): List of image filenames (up to 2).
        folder (str): Path to the folder containing the images.
    Returns:
        str: LaTeX code for the figure row.
    """
    dclass = folder.rsplit("+")[0]
    dstage = folder.rsplit("+")[1]
    
    im_file_lenght = len(images)

    if doublecol:
        latex = ""
        latex += "% Be sure to add these packages and commands in your preamble!!\n"
        latex += "% \\usepackage{caption}\n"
        latex += "% \\usepackage{subcaption}\n"
        latex += "% \\newcommand{\\vrulesep}{\\ }\n"
        latex += "% \\newcommand{\\hrulesep}{\\unskip \\ \\hrule\\ }\n"
        for count, img in enumerate(images):

            latex += "\\noindent\n"
            latex += "\\begin{minipage}{.49\\textwidth}\n"
            latex += "\t \\centering\n"
            latex += "\t \t \\hrulesep\n"
            latex += f"\t \t \\includegraphics[width=1\\linewidth]{{{super_folder}/{folder}/{img}}}\n"
            latex += "\\end{minipage}%\n"
            latex += "\\vrulesep\n"
        latex += (
            "\\captionof{figure}{"
            + "The left images in each panel are the images created by tCLEAN, the middle and right images are the models and 1d radial profiles created by FRANK of disks that are Class "
            + f"{dclass}"
            + " and Stage "
            + f"{dstage}"
            + ".}\n"
        )
    elif doublecol is False:
        latex = ""
        latex += "% Be sure to add these packages and commands in your preamble!!\n"
        latex += "% \\usepackage{caption}\n"
        latex += "% \\usepackage{subcaption}\n"
        latex += "% \\newcommand{\\vrulesep}{\\unskip \\ \\vrule\\ }\n"
        latex += "% \\newcommand{\\hrulesep}{\\unskip \\ \\hrule\\ }\n"

        for count, img in enumerate(images):

            if count == 0:
                latex += "\\noindent\n"
                latex += "\\begin{minipage}{.49\\textwidth}\n"
                latex += "\t \\centering\n"
                latex += "\t \t \\hrulesep\n"
                latex += f"\t \t \\includegraphics[width=1\\linewidth]{{{super_folder}/{folder}/{img}}}\n"
                latex += "\\end{minipage}%\n"
                latex += "\\vrulesep\n"
            elif count % 2 == 0 and count != 0 and count != (im_file_lenght - 1):
                latex += "\\vspace{0pt}\n"
                latex += "\\begin{minipage}{.49\\textwidth}\n"
                latex += "\t \\centering\n"
                latex += "\t \t \\hrulesep\n"
                latex += f"\t \t \\includegraphics[width=1\\linewidth]{{{super_folder}/{folder}/{img}}}\n"
                latex += "\\end{minipage}%\n"
                latex += "\\vrulesep\n"
            elif count % 2 != 0:
                latex += "\\begin{minipage}{.49\\textwidth}\n"
                latex += "\t \\centering\n"
                latex += "\t \t \\hrulesep\n"
                latex += f"\t \t \\includegraphics[width=1\\linewidth]{{{super_folder}/{folder}/{img}}}\n"
                latex += "\\end{minipage}%\n"
            elif count == (im_file_lenght - 1) and count % 2 == 0:
                latex += "\\vspace{0pt}\n"
                latex += "\\noindent\\makebox[\\textwidth]{%\n"
                latex += "\\begin{minipage}{.49\\textwidth}\n"
                latex += "\t \\hrulesep\n"
                latex += f"\t \\includegraphics[width=1\\linewidth]{{{super_folder}/{folder}/{img}}}\n"
                latex += "\\end{minipage}}%\n"
        latex += (
            "\\captionof{figure}{"
            + "The left images in each panel are the images created by tCLEAN, the middle and right images are the models and 1d radial profiles created by FRANK of disks that are Class "
            + f"{dclass}"
            + " and Stage "
            + f"{dstage}"
            + ".}\n"
        )
    latex += "\\vspace{0.8cm}"
    return latex


@dataclass
class GridConfig:
    reverse: bool
    doublecolumns: bool


def load_variables_grid(reverse: bool = True) -> GridConfig:
    singlecolumn = (
        input(
            "⚠️  Type 'y' or 'yes' use single column format on your grids. Anything else will cancel:\n"
        )
        .strip()
        .lower()
    )
    if singlecolumn in ["y", "yes"]:
        doublecol = False
        logger.info("Single column format enabled for LaTeX grids.")
    else:
        doublecol = True
        logger.info("Double column format enabled for LaTeX grids.")

    return GridConfig(reverse=reverse, doublecolumns=doublecol)


def generate_all_latex_figures(cfg: GridConfig) -> None:
    """
    Main latex grid image generator
    """

    if os.path.exists(paths.latex_dir):
        shutil.rmtree(paths.latex_dir)

    all_tex_path = os.path.join(paths.output_dir, "all_figures.tex")

    if os.path.exists(all_tex_path):
        os.remove(all_tex_path)

    os.makedirs(paths.latex_dir)

    if os.path.exists(pdf_dir):
        if cfg.reverse:
            # print("The files are ordered in decreasing flux order in latex files")
            logger.info("The files are ordered in decreasing flux order in latex files")
        else:
            # print("The files are ordered in increasing flux order in latex files")
            logger.info("The files are ordered in increasing flux order in latex files")

        for group in groups:
            group_path = os.path.join(pdf_dir, group)
            ## In case some of the pdf directories were not created
            if not os.path.isdir(group_path):
                # print(f"Skipping group {group} (folder not found)")
                logger.warning(f"Skipping group {group} (folder not found)")
                continue
            ## Reading every pdf image in a list
            pdf_files = sorted(os.listdir(f"{pdf_dir}/{group}"), reverse=cfg.reverse)

            ## Generating latex grid files per group
            with open(
                f"{paths.latex_dir}/{group}_generated_figures.tex",
                mode="w",
                encoding="utf-8",
            ) as f:
                f.write(
                    latex_images(
                        images=pdf_files,
                        folder=group.replace("_", "-") if "_" in group else group,
                        doublecol=cfg.doublecolumns,
                    )
                )
            ## Generating a main latex file in case You want all the grids in sequence
            ## Also good for modifying any configuration in Latex and debugging
            with open(
                f"{paths.output_dir}/all_figures.tex", "a", encoding="utf-8"
            ) as g:
                g.write(
                    "\\input{"
                    + "generated_figures_for_tex"
                    + "/"
                    + f"{group}"
                    + "_generated_figures}\n"
                )

    else:
        logger.error(
            "The latex grid files were not created, please rerun the plotting / main function setting the output as pdfs"
        )
        raise FileNotFoundError(
            "No directory called pdf, please rerun the plotting / main function setting the output as pdfs"
        )
    # print("Latex grid files generated!!")
    logger.info("Latex grid files generated!!\n" + 50 * "#")


if __name__ == "__main__":
    print(f"Running {__file__.rsplit('/',maxsplit=1)[-1]} directly")
    logger.info(f"Running {__file__.rsplit('/',maxsplit=1)[-1]} directly")


def main():
    print(f"Running {__file__.rsplit('/',maxsplit=1)[-1]} directly")
    logger.info(f"Running {__file__.rsplit('/',maxsplit=1)[-1]} directly")

    cfg = load_variables_grid(reverse=True)
    generate_all_latex_figures(cfg)
