import pandas as pd


class MovieSearch:

    def __init__(self, movies):

        self.movies = movies.copy()

        # Make sure title column is string
        self.movies["title"] = (
            self.movies["title"]
            .fillna("")
            .astype(str)
        )


    def search(self, movie_name):

        movie_name = movie_name.strip()

        if not movie_name:

            return self.movies.iloc[0:0][
                ["movieId", "title", "genres"]
            ]


        # =================================================
        # SEARCH TEXT
        # =================================================

        titles = self.movies["title"]


        # =================================================
        # 1. EXACT TITLE MATCH
        # Example:
        # Cars -> Cars
        # =================================================

        exact_match = titles.str.lower() == movie_name.lower()


        # =================================================
        # 2. TITLE STARTS WITH SEARCH
        # Example:
        # Cars 2
        # Cars 3
        # =================================================

        starts_with = (
            titles.str.lower()
            .str.startswith(movie_name.lower())
        )


        # =================================================
        # 3. TITLE CONTAINS SEARCH
        # =================================================

        contains = (
            titles.str.lower()
            .str.contains(
                movie_name.lower(),
                regex=False,
                na=False
            )
        )


        # =================================================
        # 4. CREATE RESULTS
        # =================================================

        results = self.movies[contains].copy()


        if results.empty:

            return results[
                ["movieId", "title", "genres"]
            ]


        # =================================================
        # 5. SEARCH RANKING
        # =================================================

        results["_exact"] = (
            results["title"]
            .str.lower()
            .eq(movie_name.lower())
        )


        results["_starts"] = (
            results["title"]
            .str.lower()
            .str.startswith(
                movie_name.lower()
            )
        )


        # =================================================
        # 6. SHORTER TITLE FIRST
        #
        # Cars
        # Cars 2
        # Cars 3
        # =================================================

        results["_title_length"] = (
            results["title"].str.len()
        )


        # =================================================
        # 7. SORT
        # =================================================

        results = results.sort_values(
            by=[
                "_exact",
                "_starts",
                "_title_length"
            ],
            ascending=[
                False,
                False,
                True
            ]
        )


        # =================================================
        # 8. RETURN ONLY REQUIRED COLUMNS
        # =================================================

        return results[
            ["movieId", "title", "genres"]
        ]