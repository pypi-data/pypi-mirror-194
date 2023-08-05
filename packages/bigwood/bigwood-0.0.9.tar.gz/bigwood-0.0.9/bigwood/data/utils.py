"""General purpose data utility functions
"""
import csv
import json
import time
import os
from functools import wraps
from pathlib import Path

import pandas as pd
import pyperclip

############################################
### Time Specific Utils
############################################


def daysBetween(startDate, endDate, delta=1):
    deltaDT = datetime.timedelta(days=delta)

    currentDate = startDate
    while currentDate == startDate or currentDate <= endDate:
        yield (
            currentDate,
            min(endDate, currentDate + deltaDT - datetime.timedelta(days=1)),
        )
        # yield currentDate
        currentDate += deltaDT


def timesBetween(startDateTime, endDateTime, delta=1):
    if type(delta) is datetime.timedelta:
        deltaDT = delta
    else:
        deltaDT = datetime.timedelta(days=delta)

    currentDateTime = startDateTime
    while currentDateTime == startDateTime or currentDateTime <= endDateTime:
        yield (currentDateTime, min(endDateTime, currentDateTime + deltaDT))
        # yield currentDate
        currentDateTime += deltaDT


############################################
### Reading / Writing Files
############################################


def dump_to_file(path="/tmp", dump_path="/tmp", file_format="csv", timestamp=False):
    """Write output to 'path' in 'format' if output is
    a dataframe. If you want to specify the name of the
    output file then set a .name attribute on the
    dataframe.

    Might be a good idea to add a Pickle!
    """

    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            name = getattr(args[0], "name", None)
            results = f(*args, **kwargs)

            if not Path(path).exists():
                print(f"Path: {path} does not exist")

            if isinstance(results, pd.DataFrame):
                # Create th filename
                if name and not timestamp:
                    dump_path = Path(path, f"{name}.{file_format}")
                elif name and timestamp:
                    dump_path = Path(path, f"{name}_{int(time.time())}.{file_format}")
                else:
                    dump_path = Path(path, f"{int(time.time())}.{file_format}")

                # Write file
                if format == "csv":
                    results.to_csv(dump_path)
                elif format == "json":
                    results.to_json(dump_path)
                elif format == "dict":
                    with dump_path.open("w") as file:
                        file.write(json.dumps(results.to_dict("records")))
            return results

        return wrapper

    return actual_decorator


def write_row(path: Path, header: list, row: dict):
    """Write a row to a CSV file. If the file doesn't exist then
    add a header first.

    Args:
        path (Path): path to file location.
        header (list): list of column headers
        row (dict): dict of header names and values for the row.
    """
    if not path.exists():
        with path.open(mode="w") as f:
            w = csv.DictWriter(f, fieldnames=header)
            w.writeheader()
            w.writerow(row)
    else:
        with path.open(mode="a") as f:
            w = csv.DictWriter(f, fieldnames=header)
            w.writerow(row)


############################################
### Dataframe (Pandas Utils)
############################################


def data_to_df(
    data,
    colnames: list = None,
    set_index: str = None,
    datetime_index: bool = False,
    columns_to_drop: list = None,
    map_types: dict = None,
    rename_columns: dict = None,
) -> pd.DataFrame:
    """Pandas wrapper function that saves me re-writing the same shit again and again.

    Args:
        data: Some sort of iterable object
        colnames: If you want to pass names into the dataframe. Useful if the column names are not on the
                  data i.e. with a pgcur, pass in the pgcur.description.
        set_index: column name to make index
        datetime_index: Is the index a datetime index?
        columns_to_drop: list of columns to nuke.
        map_types: Specify columns to types
        rename_columns: NOT HERE but ideally a dict of columns to rename

    Returns:
        DataFrame:
    """

    if not rename_columns:
        rename_columns = {}

    if colnames:
        results = pd.DataFrame(data, column=colnames)
    else:
        results = pd.DataFrame(data)

    if results.empty:
        return pd.DataFrame()

    if not columns_to_drop:
        columns_to_drop = []

    # convert types
    if map_types:
        for k, v in map_types.items():
            results[k] = results[k].astype(v)

    # sort index out
    if set_index and not datetime_index:
        results.index = results[set_index]
        columns_to_drop.append(set_index)
    elif set_index and datetime_index:
        results.index = pd.DatetimeIndex(results[set_index])
        columns_to_drop.append(set_index)

    # drop columns
    if columns_to_drop:
        results.drop(labels=columns_to_drop, axis=1, inplace=True)

    return results


def df_clip(df):
    """Copy a Pandas DF to the system clipboard.
    Useful for writing up tickets etc"""

    pyperclip.copy(df.to_markdown())
    print("copied")

############################################
### Path Utils
############################################


def get_folders(path, top_folder, sub_folder=None, siblings=None,  mkdir=False):
    """Within a subfolder tree with parent: top_folder, check if there
    is a sub_folder called: sub_folder. 


    data folder for syncing"""

    if isinstance(path, str):
        path = Path(path)

    path_parts = path.parts
    if top_folder not in set(path_parts):
        raise ValueError(f"{top_folder} not in project_path: {path}")

    top_folder_index = path_parts.index(top_folder)
    if top_folder_index == len(path_parts) - 1:
        raise ValueError("Not running in a sub_folder")

    if sub_folder:
        try:
            print(path_parts)
            sub_folder_index = path_parts.index(sub_folder)
        except ValueError:
            raise ValueError(f"folder {sub_folder} not present")

    if sub_folder:
        project_path = Path(*path_parts[: sub_folder_index])
    else:
        project_path = Path(*path_parts[: top_folder_index + 2])

    sib_dirs = []
    for s in siblings:
        sibling_dir = Path.joinpath(project_path, s)
        if mkdir:
            os.mkdir(sibling_dir)
        sib_dirs.append(sibling_dir)
    return *sib_dirs

