class MovieFilter:

    def __init__(self, movies, ratings):
        self.movies = movies.copy()
        self.ratings = ratings.copy()

    def filter_by_genre(self, genre):
        result = self.movies[
            self.movies["genres"]
            .str.contains(genre, case=False, na=False)
        ]

        return result

    def filter_by_year(self, year):
        result = self.movies[
            self.movies["title"]
            .str.contains(f"({year})", regex=False, na=False)
        ]

        return result

    def top_rated_movies(self, minimum_ratings=50):

        rating_stats = self.ratings.groupby("movieId").agg(
            average_rating=("rating", "mean"),
            rating_count=("rating", "count")
        ).reset_index()

        rating_stats = rating_stats[
            rating_stats["rating_count"] >= minimum_ratings
        ]

        result = self.movies.merge(
            rating_stats,
            on="movieId"
        )

        result = result.sort_values(
            "average_rating",
            ascending=False
        )

        return result