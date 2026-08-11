from database.database import get_connection


class UserManager:

    def create_user(self, username):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users (username)
                VALUES (?)
                """,
                (username,)
            )

            connection.commit()

            return cursor.lastrowid

        except Exception as error:

            print("Create user error:", error)

            return None

        finally:

            connection.close()


class FavoriteManager:

    def add_favorite(self, user_id, movie_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT OR IGNORE INTO favorites
                (user_id, movie_id)
                VALUES (?, ?)
                """,
                (user_id, movie_id)
            )

            connection.commit()

            return True

        except Exception as error:

            print("Add favorite error:", error)

            return False

        finally:

            connection.close()


    def get_favorites(self, user_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT movie_id
                FROM favorites
                WHERE user_id = ?
                ORDER BY rowid DESC
                """,
                (user_id,)
            )

            favorites = cursor.fetchall()

            return [
                movie[0]
                for movie in favorites
            ]

        except Exception as error:

            print(
                "Get favorites error:",
                error
            )

            return []

        finally:

            connection.close()


    def remove_favorite(
        self,
        user_id,
        movie_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM favorites
                WHERE user_id = ?
                AND movie_id = ?
                """,
                (user_id, movie_id)
            )

            connection.commit()

            return cursor.rowcount > 0

        except Exception as error:

            print(
                "Remove favorite error:",
                error
            )

            return False

        finally:

            connection.close()


class WatchlistManager:

    def add_to_watchlist(
        self,
        user_id,
        movie_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT OR IGNORE INTO watchlist
                (user_id, movie_id)
                VALUES (?, ?)
                """,
                (user_id, movie_id)
            )

            connection.commit()

            return True

        except Exception as error:

            print(
                "Add watchlist error:",
                error
            )

            return False

        finally:

            connection.close()


    def get_watchlist(self, user_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT movie_id
                FROM watchlist
                WHERE user_id = ?
                """,
                (user_id,)
            )

            watchlist = cursor.fetchall()

            return [
                movie[0]
                for movie in watchlist
            ]

        except Exception as error:

            print(
                "Get watchlist error:",
                error
            )

            return []

        finally:

            connection.close()


class WatchHistoryManager:

    def add_history(
        self,
        user_id,
        movie_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO watch_history
                (user_id, movie_id)
                VALUES (?, ?)
                """,
                (user_id, movie_id)
            )

            connection.commit()

            return True

        except Exception as error:

            print(
                "Add history error:",
                error
            )

            return False

        finally:

            connection.close()


    def get_history(self, user_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT movie_id, watched_at
                FROM watch_history
                WHERE user_id = ?
                ORDER BY watched_at DESC
                """,
                (user_id,)
            )

            history = cursor.fetchall()

            return history

        except Exception as error:

            print(
                "Get history error:",
                error
            )

            return []

        finally:

            connection.close()