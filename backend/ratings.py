class RatingManager:

    def __init__(self, ratings):
        self.ratings = ratings.copy()

    def get_movie_rating(self, movie_id):
        movie_ratings = self.ratings[
            self.ratings["movieId"] == movie_id
        ]

        if movie_ratings.empty:
            return None

        return round(movie_ratings["rating"].mean(), 2)

    def get_rating_count(self, movie_id):
        movie_ratings = self.ratings[
            self.ratings["movieId"] == movie_id
        ]

        return len(movie_ratings)