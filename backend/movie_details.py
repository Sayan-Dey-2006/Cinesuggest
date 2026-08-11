class MovieDetails:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_details(self, movie_id):

        movie = self.movies[
            self.movies["movieId"] == movie_id
        ]

        if movie.empty:
            return None

        movie = movie.iloc[0]

        movie_ratings = self.ratings[
            self.ratings["movieId"] == movie_id
        ]

        if movie_ratings.empty:
            average_rating = 0
            rating_count = 0
        else:
            average_rating = round(
                movie_ratings["rating"].mean(), 2
            )
            rating_count = len(movie_ratings)

        return {
            "title": movie["title"],
            "genres": movie["genres"],
            "average_rating": average_rating,
            "rating_count": rating_count
        }