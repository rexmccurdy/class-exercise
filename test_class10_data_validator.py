import pandas as pd
import pytest

from class10_data_validator import validate_columns


@pytest.fixture
def sample_df():
    """Create a small DataFrame for testing."""
    return pd.DataFrame(
        {
            "title": ["Movie A", "Movie B", "Movie C"],
            "type": ["Movie", "Movie", "Movie"],
            "release_year": [2020, 2000 ,2021],
        }
    )


def test_validate_columns_with_valid_columns(sample_df):
    # TODO 1:
    # Arrange the required column names.
    # Act by calling validate_columns().
    # Assert that the returned DataFrame has the expected columns.
    
    required_cols = ["title", "type", "release_year"]

    validated_df = validate_columns(sample_df, required_cols)

    assert validated_df.columns.tolist() == required_cols


def test_validate_columns_with_missing_column(sample_df):
    # TODO 2:
    # Use pytest.raises() to confirm that validate_columns()
    # raises ValueError when a required column is missing.
    
    with pytest.raises(ValueError):
        validate_columns(sample_df, ["title", "type", "release_year", "missing_col"])
