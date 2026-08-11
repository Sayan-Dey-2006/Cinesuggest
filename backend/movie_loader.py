import pandas as pd

class movie_loader:
    def __init__(self):
        self.movies = None
        self.ratings = None
        self.links = None
        self.tags = None

    def load_data(self):
        self.movies = pd.read_csv("data/movies.csv")
        self.ratings = pd.read_csv("data/ratings.csv")
        self.links = pd.read_csv("data/links.csv")
        self.tags = pd.read_csv("data/tags.csv")
        return {
            "Movies": self.movies,
            "Ratings": self.ratings,
            "Links": self.links,
            "Tags": self.tags
        }
