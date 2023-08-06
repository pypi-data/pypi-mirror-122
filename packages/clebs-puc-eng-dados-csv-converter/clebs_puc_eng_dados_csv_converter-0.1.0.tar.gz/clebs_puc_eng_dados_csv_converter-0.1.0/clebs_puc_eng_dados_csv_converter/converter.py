import logging
from pathlib import Path
from typing import Type

import click
import pandas as pd
from pandas.io.common import file_path_to_url

logging.basicConfig(
    level=logging.DEBUG, format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to find files to be loaded for conversion.",
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
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = "file"):
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path: %s", input_path)
    logger.info("Output path: %s", output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path or file name.")

    data = read_csv_file(source=input_path, delimiter=delimiter)
    save_to_json_files(csvs=data, output_path=output_path, prefix=prefix)


def read_csv_file(source: Path, delimiter: str = ",") -> tuple:
    """Load csv file from disk.

    Args:
        source (Path): Path containing single file or directory with multiple
            csv files to be loaded.
        delimiter (str, optional): Delimiter for columns in the csv file. Defaults to ",".
    """
    if source.is_file():
        logger.info("Reading single file %s", source)
        return (pd.read_csv(filepath_or_buffer=source, delimiter=delimiter, index_col=False),)

    logger.info("Reading all files within directory.")

    # list comprehension
    return tuple(
        [
            pd.read_csv(filepath_or_buffer=name, delimiter=delimiter, index_col=False)
            for name in source.iterdir()
        ]
    )
    
def save_to_json_files(csvs: tuple, output_path: Path, prefix: str = "file"):
    """Save dataframes to disk.

    Args:
        csvs (tuple): tuple of dataframes to be saved as json files.
        output_path (Path): Path where to save the json files
        prefix (str, optional): Prefix to be used as file name. Defaults to "file".
    """
    for i, data in enumerate(csvs):
        file_name = output_path.joinpath(f"{prefix}_{i}.json")
        logger.info("Saving file: %s ", file_name)
        
        data.to_json(
            path_or_buf=file_name, orient="records", indent=4
        )