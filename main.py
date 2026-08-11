from backend.movie_loader import movie_loader
from backend.search import MovieSearch
from backend.similarity import similarityengine
from backend.recommender import MovieRecommender
from backend.filters import MovieFilter
from backend.ratings import RatingManager
from backend.movie_details import MovieDetails

from database.database import create_tables
from database.models import (
    UserManager,
    FavoriteManager,
    WatchlistManager,
    WatchHistoryManager
)


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

create_tables()


# ==========================================
# LOAD MOVIE DATA
# ==========================================

loader = movie_loader()
data = loader.load_data()

print("\n========================================")
print("              🎬 CINESUGGEST")
print("       Movie Recommendation System")
print("========================================")

print("\nData Loaded Successfully!")
print("Movies :", len(data["Movies"]))
print("Ratings:", len(data["Ratings"]))
print("Links  :", len(data["Links"]))
print("Tags   :", len(data["Tags"]))


# ==========================================
# CREATE ENGINES
# ==========================================

search = MovieSearch(data["Movies"])

similarity_engine = similarityengine(data["Movies"])
similarity_matrix = similarity_engine.cosine_similarity()

recommender = MovieRecommender(
    data["Movies"],
    similarity_matrix
)

movie_filter = MovieFilter(
    data["Movies"],
    data["Ratings"]
)

rating_manager = RatingManager(
    data["Ratings"]
)

movie_details = MovieDetails(
    data["Movies"],
    data["Ratings"]
)


# ==========================================
# DATABASE MANAGERS
# ==========================================

user_manager = UserManager()
favorite_manager = FavoriteManager()
watchlist_manager = WatchlistManager()
history_manager = WatchHistoryManager()


# ==========================================
# CREATE USER
# ==========================================

print("\n========================================")
print("              USER SETUP")
print("========================================")

username = input("Enter your username: ").strip()

if not username:
    username = "Guest"

user_id = user_manager.create_user(username)

if user_id is None:
    print("\nUser already exists or could not be created.")

    # Existing user ID বের করার জন্য database থেকে খুঁজব
    from database.database import get_connection

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        user_id = user[0]
    else:
        user_id = 1

print(f"\nWelcome to Cinesuggest, {username}! 🎬")


# ==========================================
# MAIN MENU
# ==========================================

while True:

    print("\n")
    print("========================================")
    print("              🎬 CINESUGGEST")
    print("========================================")

    print("1.  🔍 Search Movie")
    print("2.  🎯 Get Recommendations")
    print("3.  🎭 Filter by Genre")
    print("4.  📅 Filter by Year")
    print("5.  ⭐ Top Rated Movies")
    print("6.  📊 Movie Rating")
    print("7.  🎬 Movie Details")
    print("8.  ❤️ Add Favorite")
    print("9.  📌 Add to Watchlist")
    print("10. 🕐 Add to Watch History")
    print("11. ❤️ View Favorites")
    print("12. 📌 View Watchlist")
    print("13. 🕐 View Watch History")
    print("14. 🚪 Exit")

    print("========================================")

    choice = input("Enter your choice: ")


    # ======================================
    # 1. SEARCH MOVIE
    # ======================================

    if choice == "1":

        movie_name = input(
            "\nEnter movie name: "
        )

        results = search.search(movie_name)

        if results.empty:

            print("\n❌ Movie not found.")

        else:

            print("\n🎬 Search Results:\n")
            print(
                results.to_string(index=False)
            )


    # ======================================
    # 2. RECOMMENDATIONS
    # ======================================

    elif choice == "2":

        movie_title = input(
            "\nEnter exact movie title: "
        )

        recommendations = recommender.recommend(
            movie_title
        )

        if not recommendations:

            print("\n❌ Movie not found.")

        else:

            print(
                "\n🎯 Recommended Movies:\n"
            )

            for i, movie in enumerate(
                recommendations,
                start=1
            ):

                print(
                    f"{i}. {movie['title']} | "
                    f"{movie['genres']} | "
                    f"Similarity: "
                    f"{movie['similarity']}"
                )


    # ======================================
    # 3. GENRE FILTER
    # ======================================

    elif choice == "3":

        genre = input(
            "\nEnter genre: "
        )

        results = movie_filter.filter_by_genre(
            genre
        )

        if results.empty:

            print("\n❌ No movies found.")

        else:

            print(
                f"\n🎭 Movies in {genre} genre:\n"
            )

            print(
                results[
                    ["movieId", "title", "genres"]
                ]
                .head(20)
                .to_string(index=False)
            )


    # ======================================
    # 4. YEAR FILTER
    # ======================================

    elif choice == "4":

        year = input(
            "\nEnter year: "
        )

        results = movie_filter.filter_by_year(
            year
        )

        if results.empty:

            print("\n❌ No movies found.")

        else:

            print(
                f"\n📅 Movies from {year}:\n"
            )

            print(
                results[
                    ["movieId", "title", "genres"]
                ]
                .head(20)
                .to_string(index=False)
            )


    # ======================================
    # 5. TOP RATED MOVIES
    # ======================================

    elif choice == "5":

        results = movie_filter.top_rated_movies()

        print(
            "\n⭐ TOP RATED MOVIES\n"
        )

        print(
            results[
                [
                    "title",
                    "genres",
                    "average_rating",
                    "rating_count"
                ]
            ]
            .head(20)
            .to_string(index=False)
        )


    # ======================================
    # 6. MOVIE RATING
    # ======================================

    elif choice == "6":

        try:

            movie_id = int(
                input("\nEnter Movie ID: ")
            )

            average_rating = (
                rating_manager.get_movie_rating(
                    movie_id
                )
            )

            rating_count = (
                rating_manager.get_rating_count(
                    movie_id
                )
            )

            if average_rating is None:

                print(
                    "\n❌ Rating information "
                    "not found."
                )

            else:

                print(
                    f"\n⭐ Average Rating: "
                    f"{average_rating}"
                )

                print(
                    f"👥 Number of Ratings: "
                    f"{rating_count}"
                )

        except ValueError:

            print(
                "\n❌ Please enter a valid "
                "Movie ID."
            )


    # ======================================
    # 7. MOVIE DETAILS
    # ======================================

    elif choice == "7":

        try:

            movie_id = int(
                input("\nEnter Movie ID: ")
            )

            details = movie_details.get_details(
                movie_id
            )

            if details is None:

                print(
                    "\n❌ Movie not found."
                )

            else:

                print(
                    "\n========== MOVIE DETAILS =========="
                )

                print(
                    f"🎬 Title          : "
                    f"{details['title']}"
                )

                print(
                    f"🎭 Genres         : "
                    f"{details['genres']}"
                )

                print(
                    f"⭐ Average Rating : "
                    f"{details['average_rating']}"
                )

                print(
                    f"👥 Ratings Count  : "
                    f"{details['rating_count']}"
                )

        except ValueError:

            print(
                "\n❌ Please enter a valid "
                "Movie ID."
            )


    # ======================================
    # 8. ADD FAVORITE
    # ======================================

    elif choice == "8":

        try:

            movie_id = int(
                input(
                    "\nEnter Movie ID to add "
                    "to favorites: "
                )
            )

            success = favorite_manager.add_favorite(
                user_id,
                movie_id
            )

            if success:

                print(
                    "\n❤️ Movie added to favorites!"
                )

            else:

                print(
                    "\n❌ Could not add movie."
                )

        except ValueError:

            print(
                "\n❌ Please enter a valid "
                "Movie ID."
            )


    # ======================================
    # 9. ADD TO WATCHLIST
    # ======================================

    elif choice == "9":

        try:

            movie_id = int(
                input(
                    "\nEnter Movie ID to add "
                    "to watchlist: "
                )
            )

            success = (
                watchlist_manager
                .add_to_watchlist(
                    user_id,
                    movie_id
                )
            )

            if success:

                print(
                    "\n📌 Movie added to watchlist!"
                )

            else:

                print(
                    "\n❌ Could not add movie."
                )

        except ValueError:

            print(
                "\n❌ Please enter a valid "
                "Movie ID."
            )


    # ======================================
    # 10. ADD WATCH HISTORY
    # ======================================

    elif choice == "10":

        try:

            movie_id = int(
                input(
                    "\nEnter Movie ID you watched: "
                )
            )

            success = (
                history_manager
                .add_history(
                    user_id,
                    movie_id
                )
            )

            if success:

                print(
                    "\n🕐 Watch history updated!"
                )

            else:

                print(
                    "\n❌ Could not update "
                    "watch history."
                )

        except ValueError:

            print(
                "\n❌ Please enter a valid "
                "Movie ID."
            )


    # ======================================
    # 11. VIEW FAVORITES
    # ======================================

    elif choice == "11":

        favorites = (
            favorite_manager
            .get_favorites(user_id)
        )

        if not favorites:

            print(
                "\n❤️ Your favorites list "
                "is empty."
            )

        else:

            print(
                "\n❤️ YOUR FAVORITE MOVIES\n"
            )

            for movie_id in favorites:

                movie = data["Movies"][
                    data["Movies"]["movieId"]
                    == movie_id
                ]

                if not movie.empty:

                    print(
                        f"🎬 {movie.iloc[0]['title']}"
                    )


    # ======================================
    # 12. VIEW WATCHLIST
    # ======================================

    elif choice == "12":

        watchlist = (
            watchlist_manager
            .get_watchlist(user_id)
        )

        if not watchlist:

            print(
                "\n📌 Your watchlist is empty."
            )

        else:

            print(
                "\n📌 YOUR WATCHLIST\n"
            )

            for movie_id in watchlist:

                movie = data["Movies"][
                    data["Movies"]["movieId"]
                    == movie_id
                ]

                if not movie.empty:

                    print(
                        f"🎬 {movie.iloc[0]['title']}"
                    )


    # ======================================
    # 13. VIEW WATCH HISTORY
    # ======================================

    elif choice == "13":

        history = (
            history_manager
            .get_history(user_id)
        )

        if not history:

            print(
                "\n🕐 Watch history is empty."
            )

        else:

            print(
                "\n🕐 YOUR WATCH HISTORY\n"
            )

            for movie_id, watched_at in history:

                movie = data["Movies"][
                    data["Movies"]["movieId"]
                    == movie_id
                ]

                if not movie.empty:

                    print(
                        f"🎬 {movie.iloc[0]['title']}"
                    )

                    print(
                        f"   Watched: {watched_at}"
                    )


    # ======================================
    # 14. EXIT
    # ======================================

    elif choice == "14":

        print(
            "\n========================================"
        )

        print(
            "🎬 Thank you for using Cinesuggest!"
        )

        print(
            "Goodbye! 👋"
        )

        print(
            "========================================"
        )

        break


    # ======================================
    # INVALID OPTION
    # ======================================

    else:

        print(
            "\n❌ Invalid choice."
        )

        print(
            "Please select an option from 1-14."
        )