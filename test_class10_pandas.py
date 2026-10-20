import pandas as pd
import pytest 

def test_dataframe_shape():
    # This DataFrame has 5 rows and 4 columns.
    df = pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })

    result = df.drop_duplicates()
    # assert checks a condition. If it is true, the test continues. If it is false, the test fails.
    assert result.shape == (4, 4)
    # assert df.shape == (1, 1) 

    # ^ will get an AssertionError



def test_invalid_numeric_value():
    df = pd.DataFrame({"rating": [7, "unknown", 9]})

    with pytest.raises(ValueError):
        pd.to_numeric(df["rating"])