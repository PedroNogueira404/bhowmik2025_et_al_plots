"""
Module providing a the contents table used for the plotter
function.
It takes table.csv and creates fits_files.csv, containing 202
rows, with model and data paths, and a special collumn defining
if the path is from a model or data;
Also provides full_table.csv, containing those paths
+ all the information from table_csv, with all the data per source
(half of rows from fits_files.csv)
"""

import logging
import os
import re
import pandas as pd

from bhowmik2025_et_al_plots.utils import PathUtils

logger = logging.getLogger(__name__)

paths = PathUtils()


# Check if the directory exists
def creating_tables(verbose: bool = False, debug: bool = False) -> None:
    """
    Only function of this file designed to join and manipulate tables specific
    to the data of this science case.
    """
    if not os.path.exists(paths.fits_dir):
        raise FileNotFoundError(
            f"The specified directory does not exist: {paths.fits_dir}"
        )
    if not os.path.exists(paths.data_res_dir):
        raise FileNotFoundError(
            f"The specified directory does not exist: {paths.data_res_dir}"
        )
    # Create a pandas dataframe of all .fits files in the directory,
    # with their full paths

    rows: list = []
    # COUNTER = 0
    for counter, file in enumerate(os.listdir(paths.fits_dir)):
        if file.endswith(".fits"):
            has_odisea: str = "ODISEA" in file
            # has_odisea = 0 if has_odisea else False

            has_frank: str = "frank" in file
            ismodel: bool = True if has_frank else False

            # has_iso_oph: str = "ISO_Oph" in file
            # is_iso_oph = True if has_iso_oph else False

            has_ra: str = "RA" in file
            # is_ra = True if has_ra else False

            ### YOU NEED TO CHECK IF THE NEXT CONDITIONS ARE CORRECT BY
            ### COMPARING THE TABLES (NUMBER OF ROWS)####
            if has_odisea:
                source_list: list = re.split(r"[_]+", file)[0:3]
            elif has_ra:
                source_list: list = re.split(r"[_]+", file)[0:1]
            else:
                source_list: list = re.split(r"[_]+", file)[0:2]
            #############################################################

            source = "_".join(source_list)
            # path = os.path.join(paths.fits_dir, file)
            rows.append(
                {
                    "id": counter,
                    "field": source,
                    "is model": ismodel,
                    "path": os.path.join(paths.fits_dir, file),
                }
            )
            # COUNTER += 1

    rows_rad: list = []

    for file_rad in os.listdir(paths.radial_prof_dir):
        if file_rad.endswith(".txt"):
            has_odisea: str = "ODISEA" in file_rad
            # has_iso_oph: str = "ISO_Oph" in file_rad
            has_ra: str = "RA" in file_rad

            ### YOU NEED TO CHECK IF THE NEXT CONDITIONS ARE CORRECT BY
            ### COMPARING THE TABLES (NUMBER OF ROWS)####
            if has_odisea:
                source_list: list = re.split(r"[_]+", file_rad)[0:3]
            elif has_ra:
                source_list: list = re.split(r"[_]+", file_rad)[0:1]
            else:
                source_list: list = re.split(r"[_]+", file_rad)[0:2]
            #############################################################

            source = "_".join(source_list)
            path_rad = os.path.join(paths.radial_prof_dir, file_rad)
        rows_rad.append({"field_rad": source, "path_rad": path_rad})

    rows_data_res: list = []
    for counter, file_data_res in enumerate(os.listdir(paths.data_res_dir)):
        if file_data_res.endswith(".fits"):
            # has_spec_avg_data: str = "data" in file

            has_resid: str = "residual" in file_data_res
            isres: bool = True if has_resid else False

            has_odisea: str = "ODISEA" in file_data_res
            has_ra: str = "RA" in file_data_res

            ### YOU NEED TO CHECK IF THE NEXT CONDITIONS ARE CORRECT BY
            ### COMPARING THE TABLES (NUMBER OF ROWS)####
            if has_odisea:
                source_list: list = re.split(r"[_]+", file_data_res)[0:3]
            elif has_ra:
                source_list: list = re.split(r"[_]+", file_data_res)[0:1]
            else:
                source_list: list = re.split(r"[_]+", file_data_res)[0:2]
            #############################################################

            source = "_".join(source_list)
            # path = os.path.join(paths.fits_dir, file)
            rows_data_res.append(
                {
                    # "id": counter,
                    "field_res": source,
                    "is res": isres,
                    "path_data_res": os.path.join(paths.data_res_dir, file_data_res),
                }
            )
            # COUNTER += 1

    ######### Create a pandas dataframe with the rows ###################
    ##### rows = [{"id":dummy-counter ,"field": source, "is model": bolean,
    # "path": path-to-fits-files, "path_rad": path-to-png-radial-profs}]
    table = pd.DataFrame(rows, columns=["id", "field", "is model", "path"])
    table = pd.merge(
        table, pd.DataFrame(rows_rad), left_on="field", right_on="field_rad"
    ).drop("field_rad", axis=1)
    print(table.head(), "\n")
    table = pd.merge(
        table,
        pd.DataFrame(rows_data_res),
        left_on=["field", "is model"],
        right_on=["field_res", "is res"],
    ).drop("field_res", axis=1)
    # Sorting, fixing indexes, fixing "field" problems
    table = table.sort_values(by=["field"])
    table = table.reset_index(drop=True)
    # table["id"] = table.index
    table["field"] = table["field"].str.strip().str.lower()
    ##########################################################
    # Creating a data and model identical tables to merge them again
    # keeping path of data and model in the same lines of full_table

    # table_realdata_nomodelcol = (
    #     table[table["is model"] == False]
    #     .drop("is model", axis=1)
    #     .reset_index(drop=True)
    # )
    # table_realdata_nomodelcol["id"] = table_realdata_nomodelcol.index
    ### Creating the real data table ####
    table_realdata = (
        table[(~table["is model"]) & (~table["is res"])]
        .drop(columns=["is model", "is res", "id"])
        .reset_index(drop=True)
    )
    # table_realdata["id"] = table_realdata.index
    table_realdata = table_realdata.rename(
        columns={"path": "path_data", "path_data_res": "path_avg_data"}
    )
    #### Creating the model table ####
    table_model = (
        table[table["is model"] & table["is res"]]
        .drop(columns=["is model", "is res", "id"])
        .reset_index(drop=True)
    )
    # table_model["id"] = table_model.index
    table_model = table_model.rename(
        columns={"path": "path_model", "path_data_res": "path_residual"}
    )
    # table_model = table_model.rename(
    #     columns={"path": "path_model"}
    # )
    #### IMPORTANT: table_nomodelcol is the full table predecessor,
    # before merging with the table Trisha gave me
    # Dont make confusion!!
    table_nomodelcol = pd.merge(
        table_realdata,
        table_model,
        left_on=("field", "path_rad"),
        right_on=("field", "path_rad"),
        validate="1:1",
    )
    #####################################################################

    ######### Read table that Trisha gave me ###########
    table_sizes = pd.read_csv(f"{paths.input_dir}/table.csv", index_col=False)

    # Standardize the 'field' column in table_sizes by stripping whitespace and
    # converting to lowercase
    table_sizes["field"] = table_sizes["field"].str.strip().str.lower()
    table_sizes = table_sizes.sort_values(by=["field"])
    #####################################################################

    ########## Debugging mismatches! #####################
    # Find rows in table_realdata that do not have a match
    # in table_sizes
    not_in_sizes = table_nomodelcol.merge(
        table_sizes, on=["field"], how="left", indicator=True
    ).query('_merge == "left_only"')

    # Find rows in table_sizes that do not have a match in
    # table_realdata
    not_in_realdata = table_sizes.merge(
        table_nomodelcol, on=["field"], how="left", indicator=True
    ).query('_merge == "left_only"')

    if debug:

        print("Rows in table_realdata not in table_sizes:")
        print(not_in_sizes)

        print("\nRows in table_sizes not in table_realdata:")
        print(not_in_realdata)

    ########## Merge the two tables ##############################
    if not_in_sizes.empty and not_in_realdata.empty:
        # print("There is no mismatch - It is safe to merge!!", "\n", 50 * "#")
        logger.info("There is no mismatch - It is safe to merge!!")

        full_table = pd.merge(
            table_nomodelcol,
            table_sizes,
            left_on=("field"),
            right_on=("field"),
            validate="1:1",
        )
    else:
        logger.error("Mismatch found in sizes or realdata. Aborting merge.")
        raise ValueError("Mismatch found in sizes or realdata. Aborting merge.")

    table_nomodelcol.to_csv(f"{paths.input_dir}/table_paths.csv", index=False)
    logger.info("Saved table_paths.csv successfully!")
    if verbose:
        print(
            50 * "#",
            "\n",
            "Saved table_paths.csv successfully!",
            table_nomodelcol.info(verbose=verbose),
            "\n",
            50 * "#",
        )
    #####################################################################

    ####Now fix the center_x and center_y for using of astropy before exporting
    # full table:
    def fix_center_x(s):
        """
        If there are 3 colons, replace the last colon with a dot
        """
        if s.count(":") == 3:
            s = s[::-1].replace(":", ".", 1)[::-1]
        return s

    def fix_center_y(s):
        """
        Replace the first two dots with colons
        """
        return s.replace(".", ":", 2)

    # Apply to my DataFrame
    full_table["center_x"] = full_table["center_x"].astype(str).apply(fix_center_x)
    full_table["center_y"] = full_table["center_y"].astype(str).apply(fix_center_y)

    full_table["Class"] = full_table["Class"].replace({"I": "I_F", "F": "I_F"})
    full_table["Group"] = full_table["Stage"].astype(str) + "+" + full_table["Class"]
    full_table["Group"] = full_table["Group"].str.strip()

    # table.to_csv(f"{paths.input_dir}/fits_files.csv", index=False)
    # logger.info("Saved table.csv successfully!")
    # if verbose:

    #     print(
    #         50 * "#",
    #         "\n",
    #         "Saved table.csv successfully!",
    #         table.info(verbose=verbose),
    #         "\n",
    #         50 * "#",
    #     )
    # else:
    #     print(
    #         50 * "#",
    #         "\n",
    #         "Saved full_table.csv successfully!",
    #         "\n",
    #         50 * "#",
    #     )
    full_table.to_csv(f"{paths.input_dir}/full_table.csv", index=False)
    logger.info("Saved full_table.csv successfully!")
    if verbose:
        print(
            50 * "#",
            "\n",
            "Saved full_table.csv successfully!",
            full_table.info(verbose=verbose),
            "\n",
            50 * "#",
        )
    # else:
    #     print(
    #         50 * "#",
    #         "\n",
    #         "Saved full_table.csv successfully!",
    #         "\n",
    #         50 * "#",
    #     )


if __name__ == "__main__":
    print(f"\nRunning {__file__.rsplit('/',maxsplit=1)[-1]} directly\n")
    creating_tables(verbose=True, debug=False)


def main():
    print(f"\nRunning {__file__.rsplit('/',maxsplit=1)[-1]} directly\n")
    creating_tables(verbose=True, debug=False)
