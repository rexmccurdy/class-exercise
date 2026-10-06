import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    filepath = Path(args.input)

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
    logger.info(f"Data loaded from {filepath}")

    # TODO 4:
    # Create a Path object from args.input.
    # Inside a try block, load that path using pd.read_csv().
    # Catch FileNotFoundError, log an ERROR message,
    # and exit with sys.exit(1).
    # Log an INFO message.

    df_original = df.copy()


    show_overview(df)
    logger.info("Initial overview of data")

    # TODO 5:
    # Call show_overview().
    # Log an INFO message.
    step_1_len = len(df)
    df = remove_duplicates(df)
    logger.info(f"Dropped {step_1_len - len(df)} duplicate rows")

    step_2_len = len(df)
    df = drop_missing_rows(df)
    logger.info(f"Dropped {step_2_len - len(df)} rows with missing values")

    try:
        df = remove_iqr_outliers(df, "runtime_minutes", 1.5)
    except ValueError as error:
        logger.info(error)
        sys.exit(1)


    for col in ["title", "type", "country"]:
        df[col].apply(clean_text)
        logger.info(f"{col} column cleaned")

    report = {"rows_before": len(df_original), "rows_after": len(df), "rows_removed": len(df_original) - len(df), "columns": df.columns}
    logger.info(f"report: {report}")
     
     
        # TODO 3:
    # Inside a try block, remove runtime_minutes outliers
    # using remove_iqr_outliers() with a threshold of 1.5.
    # Catch ValueError and exit with sys.exit(1).# Log an INFO message.

    # TODO 4:
    # Apply clean_text() to title, type, and country.
    # Log an INFO message.

    # TODO 5:
    # Create a report (dictionary) containing rows_before, rows_after, rows_removed, and columns.
    # Log an INFO message reporting: rows_before, rows_after, rows_removed, and columns.
    






if __name__ == "__main__":
    main()
