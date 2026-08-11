from backend import similarity

class MovieRecommender:
    def __init__(self, movies, similarity_matrix):
        self.movies = movies.reset_index(drop=True)
        self.similarity_matrix = similarity_matrix

        self.movie_indices = {
            title.lower(): index for index, title in enumerate(movies["title"])
        }

    def recommend(self, movie_title, number_of_movies=10):
        movie_title = movie_title.lower().strip()
        if movie_title not in self.movie_indices:
            return []

        movie_index = self.movie_indices[movie_title]
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))

        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        similarity_movies = similarity_scores[1:number_of_movies+1]
        recommendations = []
        for index, score in similarity_movies:
            movie = self.movies.iloc[index]
            recommendations.append({
                "title": movie["title"],
                "genres": movie["genres"],
                "similarity": round(float(score), 3)
            })

        return recommendations
