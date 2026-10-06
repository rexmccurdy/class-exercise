import logging

import re

import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug(f"shape of df: {df.shape}")
    print(df.shape)
    print(df.head)
    print(df.columns)
    print(df.dtypes)

    # TODO 1:
    # Log a DEBUG message containing the shape.
    # Print the shape, first five rows, column names, and data types.


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    len_before = len(df)
    df = df.drop_duplicates()
    logger.debug(f"df reduced from {len_before} to {len(df)} rows by dropping duplicates")
    return df

    # TODO 2:
    # Remove exact duplicate rows.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    len_before = len(df)
    df = df.dropna()
    logger.debug(f"df reduced from {len_before} to {len(df)} rows by dropping missing values")
    return df


    # TODO 3:
    # Drop rows containing one or more missing values.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    

def clean_text(value):
    """Normalize one text value."""

    vlue = value.str.strip()
    value = value.str.lower()
    value = re.sub(r"/s+", " ", value)
    return value

    # TODO 1:
    # Strip surrounding whitespace.
    # Convert text to lowercase.
    # Collapse repeated whitespace.


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""

    if column not in df:
        logger.error("Column does not exsist")
        raise ValueError

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantil(0.75)
    iqr = q3 - q1
    low = q1 - threshold * iqr
    high = q3 + threshold * iqr

    cut_df = df[(df[column] >= low) & (df[column] <= high)]
    logger.debug(f"IQR bounds of {low} and {high} removed {len(df) - len(cut_df)} outliers")
    return df

    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    
