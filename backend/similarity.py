from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
class similarityengine:
    def __init__(self,movies):
        self.movies = movies.copy()

    def cosine_similarity(self):
        self.movies["genres"]=self.movies["genres"].fillna("")
        tfidf=TfidfVectorizer(stop_words='english')
        tfidf_matrix=tfidf.fit_transform(self.movies["genres"])

        similarity=cosine_similarity(tfidf_matrix,tfidf_matrix)

        return similarity
