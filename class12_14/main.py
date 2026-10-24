from fastapi import FastAPI, Query
from src import MovieInput, MovieResponse, DataStorage, CSVInfo
import logging
import io
import pandas as pd
from fastapi import File, UploadFile, HTTPException
from pathlib import Path



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie API")
storage = DataStorage()

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int):
    return {"requested_id": movie_id}

@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record




@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    result = list(movies.values())[:limit]
    logger.info(f"Returning {len(result)} movies")
 
    return result


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    movie_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record
    logger.info(f"Added movie with ID {movie_id}")
    return record


@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}

@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException( status_code=404, detail="04dd")

    return movie

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    file_path = Path(file.filename)
    if file_path.suffix != ".csv":
        logger.warning(f"Rejected non-CSV file: {file_path}")
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
        logger.warning(f"Failed to read {file_path}: {error}")
        raise HTTPException(status_code=400, detail="Failed to read CSV file.")


    storage.save_data(df, file_path)
    dataset_id = storage.save_data(df, file.filename)
    logger.info(f"Saved data with ID: {dataset_id} from filename: {file_path}")

    return CSVInfo(
        dataset_id=dataset_id,
        filename=file_path,
        shape=df.shape,
        column_names=df.columns.tolist()
    )

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    df = storage.get_data(dataset_id)
    if df is None:
        logger.warning(f"Data set with ID {dataset_id} is missing")
        raise HTTPException(status_code=404, detail = "Failed to retrieve data")

    else:
        logger.info(f"Successfully retrieved data set with ID: {dataset_id}")

    return {
        "dataset_id": dataset_id,
        "rows": len(df),
        "columns": df.columns.tolist()
    }
    # TODO 5: get the DataFrame using storage.get_data().
    # If it is missing, log a WARNING and raise HTTPException with status 404.
    # Otherwise, log successful retrieval at INFO.
    # Return a dictionary with dataset_id, rows, and columns.
    
