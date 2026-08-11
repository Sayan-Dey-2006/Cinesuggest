# ============================================================
# CINESUGGEST - MAIN FLASK APPLICATION
# ============================================================

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

import os
import re
import requests
import pandas as pd

from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.movie_loader import movie_loader
from backend.recommender import MovieRecommender
from backend.similarity import similarityengine

from database.database import create_tables
from database.models import (
    FavoriteManager,
    WatchlistManager
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

TMDB_FIND_URL = "https://api.themoviedb.org/3/find"


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# DATABASE
# ============================================================

create_tables()


# ============================================================
# LOAD MOVIE DATA
# ============================================================

print("==============================================")
print("          CINESUGGEST STARTING")
print("==============================================")

loader = movie_loader()

data = loader.load_data()

movies = data["Movies"]
links = data["Links"]
ratings = data["Ratings"]

print("Movies loaded:", len(movies))
print("Movie columns:", list(movies.columns))
print("Links columns:", list(links.columns))


# ============================================================
# RATING MAP
# ============================================================

rating_map = {}


def load_ratings():

    global rating_map

    try:

        if (
            ratings is not None
            and "movieId" in ratings.columns
            and "rating" in ratings.columns
        ):

            average_ratings = (
                ratings
                .groupby("movieId")["rating"]
                .mean()
            )

            rating_map = (
                average_ratings
                .round(1)
                .to_dict()
            )

            print(
                "Average ratings loaded:",
                len(rating_map)
            )

            return

    except Exception as error:

        print(
            "Rating loading error:",
            error
        )

    print(
        "WARNING: Rating data could not be loaded."
    )


load_ratings()


# ============================================================
# SIMILARITY ENGINE
# ============================================================

print("Creating similarity engine...")

similarity_engine = similarityengine(movies)

similarity_matrix = (
    similarity_engine.cosine_similarity()
)

print("Similarity matrix created!")


# ============================================================
# RECOMMENDER
# ============================================================

recommender = MovieRecommender(
    movies,
    similarity_matrix
)


# ============================================================
# DATABASE MANAGERS
# ============================================================

favorite_manager = FavoriteManager()

watchlist_manager = WatchlistManager()


# ============================================================
# DEMO USER
# ============================================================

USER_ID = 1


# ============================================================
# CACHE
# ============================================================

tmdb_cache = {}
poster_cache = {}


# ============================================================
# NORMALIZE TITLE
# ============================================================

def normalize_title(title):

    if not title:
        return ""

    title = str(title).lower().strip()

    title = re.sub(
        r"\s*\(\d{4}\)\s*$",
        "",
        title
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title.strip()


# ============================================================
# GET IMDB ID
# ============================================================

# ============================================================
# GET IMDB ID
# ============================================================

# ============================================================
# GET IMDB ID
# ============================================================

def get_imdb_id(movie_id):

    try:

        movie_id = int(movie_id)

        movie_link = links[
            links["movieId"] == movie_id
        ]

        if movie_link.empty:
            return None

        imdb_id = movie_link.iloc[0]["imdbId"]

        if pd.isna(imdb_id):
            return None

        # Convert safely
        try:
            imdb_number = int(float(imdb_id))
        except (ValueError, TypeError):
            return None

        # IMDb IDs in MovieLens may have leading zeros removed.
        # IMDb numeric part is 7 digits.
        imdb_number_str = str(imdb_number).zfill(7)

        return "tt" + imdb_number_str

    except Exception as error:

        print(
            "IMDB ID error:",
            error
        )

        return None
# ============================================================
# GET TMDB INFORMATION
# ============================================================

# ============================================================
# GET TMDB INFORMATION
# ============================================================

def get_tmdb_info(imdb_id):

    if not TMDB_API_KEY:
        return {
            "poster": None,
            "rating": None
        }

    if not imdb_id:
        return {
            "poster": None,
            "rating": None
        }

    imdb_id = str(imdb_id).strip()

    if not imdb_id.startswith("tt"):
        imdb_id = "tt" + imdb_id

    # Cache
    if imdb_id in tmdb_cache:
        return tmdb_cache[imdb_id]

    try:

        url = f"{TMDB_FIND_URL}/{imdb_id}"

        params = {
            "api_key": TMDB_API_KEY,
            "external_source": "imdb_id"
        }

        response = requests.get(
            url,
            params=params,
            timeout=2
        )

        print("IMDB:", imdb_id)
        print("TMDB STATUS:", response.status_code)

        if response.status_code != 200:

            print(
                "TMDB HTTP error:",
                response.status_code
            )

            result = {
                "poster": None,
                "rating": None
            }

            tmdb_cache[imdb_id] = result

            return result

        # Safely decode JSON
        try:

            response_data = response.json()

        except Exception as error:

            print(
                "TMDB JSON error:",
                error
            )

            result = {
                "poster": None,
                "rating": None
            }

            tmdb_cache[imdb_id] = result

            return result

        movie_results = response_data.get(
            "movie_results",
            []
        )

        # No movie found
        if not movie_results:

            print(
                "TMDB: Movie not found:",
                imdb_id
            )

            result = {
                "poster": None,
                "rating": None
            }

            tmdb_cache[imdb_id] = result

            return result

        movie = movie_results[0]

        # ====================================================
        # POSTER
        # ====================================================

        poster_path = movie.get(
            "poster_path"
        )

        if poster_path:

            poster_url = (
                TMDB_IMAGE_BASE_URL
                + str(poster_path)
            )

        else:

            poster_url = None

        # ====================================================
        # RATING
        # ====================================================

        tmdb_rating = movie.get(
            "vote_average"
        )

        try:

            if tmdb_rating is not None:

                tmdb_rating = round(
                    float(tmdb_rating),
                    1
                )

        except (
            ValueError,
            TypeError
        ):

            tmdb_rating = None

        # ====================================================
        # FINAL RESULT
        # ====================================================

        result = {
            "poster": poster_url,
            "rating": tmdb_rating
        }

        tmdb_cache[imdb_id] = result

        return result

    except Exception as error:

        print(
            "TMDB request error:",
            repr(error)
        )

        result = {
            "poster": None,
            "rating": None
        }

        tmdb_cache[imdb_id] = result

        return result

# ============================================================
# GET MOVIE INFO
# ============================================================

def get_movie_info(movie_id):

    movie_id = int(movie_id)

    imdb_id = get_imdb_id(movie_id)

    if not imdb_id:

        return {
            "poster": None,
            "rating": None
        }

    return get_tmdb_info(imdb_id)


# ============================================================
# GET MOVIE POSTER
# ============================================================

def get_movie_poster(movie_id):

    movie_id = int(movie_id)

    if movie_id in poster_cache:
        return poster_cache[movie_id]

    info = get_movie_info(movie_id)

    poster = info.get("poster")

    poster_cache[movie_id] = poster

    return poster


# ============================================================
# GET MOVIE RATING
# ============================================================

def get_movie_rating(movie_id):

    movie_id = int(movie_id)

    if movie_id in rating_map:

        return rating_map[movie_id]

    imdb_id = get_imdb_id(movie_id)

    if not imdb_id:
        return None

    info = get_tmdb_info(imdb_id)

    return info.get("rating")


# ============================================================
# MOVIE TO DICTIONARY
# ============================================================

def movie_to_dict(movie):

    try:

        movie_id = int(
            movie["movieId"]
        )

    except Exception:

        return None

    title = str(
        movie.get(
            "title",
            "Unknown Movie"
        )
    )

    genres = str(
        movie.get(
            "genres",
            "Unknown"
        )
    )

    return {

        "movieId": movie_id,

        "title": title,

        "genres": genres,

        "poster": get_movie_poster(
            movie_id
        ),

        "rating": get_movie_rating(
            movie_id
        )

    }


# ============================================================
# FAST SEARCH
# ============================================================

def fast_movie_search(query):

    query = normalize_title(query)

    if not query:
        return movies.head(0)

    df = movies.copy()

    df["_normalized_title"] = (
        df["title"]
        .fillna("")
        .astype(str)
        .apply(normalize_title)
    )

    exact = df[
        df["_normalized_title"] == query
    ]

    starts = df[
        df["_normalized_title"].str.startswith(
            query,
            na=False
        )
        &
        (
            df["_normalized_title"] != query
        )
    ]

    contains = df[
        df["_normalized_title"].str.contains(
            query,
            case=False,
            regex=False,
            na=False
        )
        &
        ~df.index.isin(exact.index)
        &
        ~df.index.isin(starts.index)
    ]

    result = pd.concat(
        [
            exact,
            starts,
            contains
        ]
    )

    result = result[
        ~result.index.duplicated(
            keep="first"
        )
    ]

    result = result.drop(
        columns=[
            "_normalized_title"
        ],
        errors="ignore"
    )

    return result.head(20)


# ============================================================
# FAST MOVIE CONVERSION
# ============================================================

def movies_to_dict_fast(movie_df):

    if movie_df is None or movie_df.empty:
        return []

    # Maximum 20 movies only
    movie_df = movie_df.head(20)

    results = []

    with ThreadPoolExecutor(
        max_workers=30
    ) as executor:

        futures = {
            executor.submit(
                movie_to_dict,
                movie
            ): index

            for index, (_, movie)
            in enumerate(
                movie_df.iterrows()
            )
        }

        temp_results = {}

        for future in as_completed(futures):

            index = futures[future]

            try:

                result = future.result()

                if result:
                    temp_results[index] = result

            except Exception as error:

                print(
                    "Movie conversion error:",
                    error
                )

    # Keep original movie order
    for index in sorted(temp_results):

        results.append(
            temp_results[index]
        )

    return results
# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )
# ============================================================
# FAVORITES PAGE
# ============================================================

@app.route("/favorites")
def favorites_page():

    return render_template(
        "favorites.html"
    )


# ============================================================
# WATCHLIST PAGE
# ============================================================

@app.route("/watchlist")
def watchlist_page():

    return render_template(
        "watchlist.html"
    )

# ============================================================
# GET FAVORITES
# ============================================================

@app.route("/api/favorites", methods=["GET"])
def get_favorites():

    try:

        movie_ids = favorite_manager.get_favorites(USER_ID)

        result = []

        for movie_id in movie_ids:

            movie = movies[
                movies["movieId"] == movie_id
            ]

            if movie.empty:
                continue

            movie = movie.iloc[0]

            movie_result = movie_to_dict(movie)

            if movie_result:
                result.append(movie_result)

        return jsonify(result)

    except Exception as error:

        print("Favorites loading error:", error)

        return jsonify({
            "error": "Could not load favorites"
        }), 500


# ============================================================
# GET WATCHLIST
# ============================================================

@app.route("/api/watchlist", methods=["GET"])
def get_watchlist():

    try:

        movie_ids = watchlist_manager.get_watchlist(USER_ID)

        result = []

        for movie_id in movie_ids:

            movie = movies[
                movies["movieId"] == movie_id
            ]

            if movie.empty:
                continue

            movie = movie.iloc[0]

            movie_result = movie_to_dict(movie)

            if movie_result:
                result.append(movie_result)

        return jsonify(result)

    except Exception as error:

        print("Watchlist loading error:", error)

        return jsonify({
            "error": "Could not load watchlist"
        }), 500
# ============================================================
# MOVIE DETAILS PAGE
# ============================================================

@app.route("/movie/<int:movie_id>")
def movie_details_page(movie_id):

    return render_template(
        "movie_details.html",
        movie_id=movie_id
    )


# ============================================================
# SEARCH API
# ============================================================

@app.route("/api/search")
def search_movies():

    movie_name = request.args.get(
        "query",
        ""
    ).strip()

    if not movie_name:
        return jsonify([])

    try:

        results = fast_movie_search(
            movie_name
        )

        if results.empty:
            return jsonify([])

        return jsonify(
            movies_to_dict_fast(results)
        )

    except Exception as error:

        print(
            "Search error:",
            error
        )

        return jsonify({
            "error": "Search failed"
        }), 500


# ============================================================
# RECOMMENDATION API
# ============================================================

@app.route("/api/recommend")
def recommend_movies():

    movie_title = request.args.get(
        "title",
        ""
    ).strip()

    if not movie_title:
        return jsonify([])

    try:

        recommendations = recommender.recommend(
            movie_title
        )

        if isinstance(
            recommendations,
            pd.DataFrame
        ):

            recommendations = (
                recommendations
                .to_dict(
                    orient="records"
                )
            )

        if not recommendations:
            return jsonify([])

        result = []

        for movie in recommendations:

            if isinstance(
                movie,
                pd.Series
            ):

                movie = movie.to_dict()

            movie_id = movie.get(
                "movieId"
            )

            if movie_id is None:
                continue

            try:

                movie_id = int(movie_id)

            except Exception:

                continue

            result.append({

                "movieId": movie_id,

                "title": str(
                    movie.get(
                        "title",
                        "Unknown Movie"
                    )
                ),

                "genres": str(
                    movie.get(
                        "genres",
                        "Unknown"
                    )
                ),

                "poster": get_movie_poster(
                    movie_id
                ),

                "rating": get_movie_rating(
                    movie_id
                )

            })

            if len(result) >= 20:
                break

        return jsonify(result)

    except Exception as error:

        print(
            "Recommendation error:",
            error
        )

        return jsonify({
            "error":
                "Recommendation failed"
        }), 500


# ============================================================
# TOP RATED MOVIES
# ============================================================

@app.route("/api/top-rated")
def top_rated_movies():

    try:

        if not rating_map:
            return jsonify([])

        rating_df = pd.DataFrame(
            list(rating_map.items()),
            columns=[
                "movieId",
                "rating"
            ]
        )

        rating_df["rating"] = pd.to_numeric(
            rating_df["rating"],
            errors="coerce"
        )

        rating_df = (
            rating_df
            .dropna(
                subset=["rating"]
            )
            .sort_values(
                "rating",
                ascending=False
            )
            .head(20)
        )

        result = []

        for _, row in rating_df.iterrows():

            movie_id = int(
                row["movieId"]
            )

            movie = movies[
                movies["movieId"] == movie_id
            ]

            if movie.empty:
                continue

            movie_result = movie_to_dict(
                movie.iloc[0]
            )

            if movie_result:

                movie_result["rating"] = round(
                    float(row["rating"]),
                    1
                )

                result.append(
                    movie_result
                )

        return jsonify(result)

    except Exception as error:

        print(
            "Top rated error:",
            error
        )

        return jsonify({
            "error":
                "Could not load top rated movies"
        }), 500


# ============================================================
# GENRE API
# ============================================================

@app.route("/api/genre/<path:genre>")
def movies_by_genre(genre):

    try:

        genre = genre.strip()

        if not genre:
            return jsonify([])

        genre_movies = movies[
            movies["genres"]
            .fillna("")
            .astype(str)
            .str.contains(
                genre,
                case=False,
                regex=False,
                na=False
            )
        ]

        genre_movies = genre_movies.head(20)

        return jsonify(
            movies_to_dict_fast(
                genre_movies
            )
        )

    except Exception as error:

        print(
            "Genre error:",
            error
        )

        return jsonify({
            "error":
                "Could not load genre movies"
        }), 500


# ============================================================
# MOVIE DETAILS API
# ============================================================

@app.route("/api/movie/<int:movie_id>")
def movie_details_api(movie_id):

    try:

        movie = movies[
            movies["movieId"] == movie_id
        ]

        if movie.empty:

            return jsonify({
                "error": "Movie not found"
            }), 404

        movie = movie.iloc[0]

        result = movie_to_dict(movie)

        return jsonify(result)

    except Exception as error:

        print(
            "Movie details error:",
            error
        )

        return jsonify({
            "error":
                "Could not load movie details"
        }), 500


# ============================================================
# FAVORITE ADD API
# ============================================================

@app.route(
    "/api/favorites/add",
    methods=["POST"]
)
def add_favorite():

    try:

        data = request.get_json()

        movie_id = int(
            data.get("movieId")
        )

        result = favorite_manager.add_favorite(
            USER_ID,
            movie_id
        )

        if result is None:
            return jsonify({
                "success": True
            })

        if isinstance(result, bool):

            return jsonify({
                "success": result
            })

        return jsonify({
            "success": True
        })

    except Exception as error:

        print(
            "Favorite error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Could not add movie to favorites."
        }), 500

    # ============================================================
    # WATCHLIST ADD API
    # ============================================================
@app.route("/api/watchlist/add", methods=["POST"])
def add_watchlist():
    try:
        data = request.get_json()
        movie_id = int(data.get("movieId"))

        result = watchlist_manager.add_to_watchlist(USER_ID, movie_id)

        if result is None:
            return jsonify({"success": True})

        if isinstance(result, bool):
            return jsonify({"success": result})

        return jsonify({"success": True})

    except Exception as error:
        print("Watchlist error:", error)
        return jsonify({
            "success": False,
            "message": "Could not add movie to watchlist."
        }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    print()
    print("==============================================")
    print("             CINESUGGEST READY")
    print("==============================================")
    print()

    print("Open: http://127.0.0.1:5000")
    print()

    if TMDB_API_KEY:
        print("TMDB API key loaded successfully!")
    else:
        print("WARNING: TMDB API key not found!")

    print()
    print("==============================================")

    app.run(debug=True)
