import logging
import sys
from pathlib import Path
from typing import Type, Union

import click
import pandas as pd
from pandas.core.frame import DataFrame

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where the files will be loaded for conversion.",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to split the files.",
    type=str,
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        " The suffix will be a number starting from 0. ge: file_0.json."
    ),
)
def converter(
    input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = None
):
    """Convert Single file or list of CSV files to json."""
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path %s", input_path)
    logger.info("Output path %s", output_path)
    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise (TypeError("Not a valid path or file name.", p))

    data = read_csv_file(source=input_path, delimiter=delimiter)
    save_to_json_files(data, output_path, prefix)


def read_csv_file(source: Path, delimiter: str) -> tuple:
    """Load csv files from disk.

    Args:
        source (Path): Path of a single csv file or a directory containing csv files.
        delimiter (str): Separator for columns in csv.

    Return:
        tuple: tuple of DataFrames.
    """
    if source.is_file():
        logger.info("Reading single file %s", source)
        return (
            pd.read_csv(
                filepath_or_buffer=source, delimiter=delimiter, index_col=False
            ),
        )

    logger.info("Reading all files within subdirectory %s", source)
    data = tuple(
        [
            pd.read_csv(filepath_or_buffer=name, delimiter=delimiter, index_col=False)
            for name in source.iterdir()
        ]
    )
    return data


def save_to_json_files(csvs: tuple, output_path: Path, prefix: str = None):
    """Save dataframes to Disk.

    Args:
        csvs (tuple): Tuple with dataframes that will be converted
        output_path (Path): Path where to save the json files
        file_names (str): Name of files. If nothing is given it will
    """
    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json"
        logger.info("Saving file %s in folder %s", file_name, output_path)

        data: pd.DataFrame = csvs[i]
        data.to_json(
            path_or_buf=output_path.joinpath(file_name),
            orient="records",
            indent=4,
        )
        i += 1
