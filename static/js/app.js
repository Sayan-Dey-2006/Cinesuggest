// =====================================================
// CINESUGGEST - MAIN JAVASCRIPT
// =====================================================

let currentMovies = [];


// =====================================================
// PAGE LOAD
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Cinesuggest JavaScript loaded!");

    setupNavigation();
    setupSearch();
    setupGenreButtons();
    setupViewAllButtons();

    loadRecommendedMovies();
    loadTopRatedMovies();

});


// =====================================================
// NAVIGATION
// =====================================================

function setupNavigation() {

    const navLinks =
        document.querySelectorAll(".navbar nav a");

    navLinks.forEach(function (link) {

        const text =
            link.innerText.toLowerCase();

        if (text.includes("home")) {

            link.addEventListener("click", function (event) {

                event.preventDefault();

                window.location.href = "/";

            });

        }

        else if (text.includes("top rated")) {

            link.addEventListener("click", function (event) {

                event.preventDefault();

                const section =
                    document.getElementById("topRatedGrid");

                if (section) {

                    section.scrollIntoView({
                        behavior: "smooth"
                    });

                }

            });

        }

    });

}


// =====================================================
// SEARCH
// =====================================================

function setupSearch() {

    const searchInput =
        document.getElementById("searchInput");

    const searchButton =
        document.getElementById("searchButton");


    if (!searchInput || !searchButton) {

        console.log("Search elements not found.");

        return;

    }


    searchButton.addEventListener("click", function () {

        searchMovies(searchInput.value);

    });


    searchInput.addEventListener("keydown", function (event) {

        if (event.key === "Enter") {

            searchMovies(searchInput.value);

        }

    });

}


// =====================================================
// SEARCH MOVIES
// =====================================================

async function searchMovies(query) {

    query = query.trim();


    if (!query) {

        alert("Please enter a movie name.");

        return;

    }


    try {

        const response =
            await fetch(
                `/api/search?query=${encodeURIComponent(query)}`
            );


        const data =
            await response.json();


        if (!response.ok || !Array.isArray(data)) {

            throw new Error("Search failed");

        }


        currentMovies = data;


        displayMovies(
            data,
            `Search Results for "${query}"`,
            true
        );


    }

    catch (error) {

        console.error("Search error:", error);

        alert("Could not search movies.");

    }

}


// =====================================================
// RECOMMENDED MOVIES
// =====================================================

async function loadRecommendedMovies() {

    const grid =
        document.getElementById(
            "recommendationGrid"
        );


    if (!grid) {

        return;

    }


    try {

        const searchResponse =
            await fetch(
                "/api/search?query=toy"
            );


        const searchData =
            await searchResponse.json();


        if (
            !searchResponse.ok ||
            !Array.isArray(searchData) ||
            searchData.length === 0
        ) {

            return;

        }


        const firstMovie =
            searchData.find(function (movie) {

                return getMovieId(movie) !== null;

            });


        if (!firstMovie) {

            return;

        }


        const recommendationResponse =
            await fetch(
                `/api/recommend?title=${encodeURIComponent(firstMovie.title)}`
            );


        const recommendations =
            await recommendationResponse.json();


        if (
            recommendationResponse.ok &&
            Array.isArray(recommendations) &&
            recommendations.length > 0
        ) {

            displayMoviesInGrid(
                recommendations,
                grid
            );

        }

    }

    catch (error) {

        console.error(
            "Recommendation error:",
            error
        );

    }

}


// =====================================================
// TOP RATED
// =====================================================

async function loadTopRatedMovies() {

    const grid =
        document.getElementById(
            "topRatedGrid"
        );


    if (!grid) {

        return;

    }


    try {

        const response =
            await fetch(
                "/api/top-rated"
            );


        const movies =
            await response.json();


        if (
            !response.ok ||
            !Array.isArray(movies)
        ) {

            throw new Error(
                "Top rated request failed"
            );

        }


        if (movies.length > 0) {

            displayMoviesInGrid(
                movies,
                grid
            );

        }

    }

    catch (error) {

        console.error(
            "Top rated error:",
            error
        );

    }

}


// =====================================================
// GENRE BUTTONS
// =====================================================

function setupGenreButtons() {

    const genreButtons =
        document.querySelectorAll(".genre-card");

    genreButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const genre =
                button.dataset.genre;

            console.log("Genre selected:", genre);

            if (!genre) {
                return;
            }

            loadGenreMovies(genre);

        });

    });

}


// =====================================================
// LOAD GENRE MOVIES
// =====================================================

async function loadGenreMovies(genre) {

    try {

        const response =
            await fetch(
                `/api/genre/${encodeURIComponent(genre)}`
            );


        const movies =
            await response.json();


        if (
            !response.ok ||
            !Array.isArray(movies)
        ) {

            throw new Error(
                "Genre request failed"
            );

        }


        currentMovies = movies;


        displayMovies(
            movies,
            `${genre} Movies`,
            true
        );


    }

    catch (error) {

        console.error(
            "Genre error:",
            error
        );

        alert(
            "Could not load movies for this genre."
        );

    }

}


// =====================================================
// VIEW ALL / EXPLORE
// =====================================================

function setupViewAllButtons() {

    const buttons =
        document.querySelectorAll(
            ".view-all"
        );


    buttons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const text =
                    button.innerText.toLowerCase();


                if (
                    text.includes("explore")
                ) {

                    const section =
                        document.getElementById(
                            "topRatedGrid"
                        );


                    if (section) {

                        section.scrollIntoView({
                            behavior: "smooth"
                        });

                    }

                }

                else {

                    const section =
                        document.getElementById(
                            "recommendationGrid"
                        );


                    if (section) {

                        section.scrollIntoView({
                            behavior: "smooth"
                        });

                    }

                }

            }
        );

    });

}


// =====================================================
// MOVIE ID HELPER
// =====================================================

function getMovieId(movie) {

    if (
        !movie ||
        typeof movie !== "object"
    ) {

        return null;

    }


    const id =
        movie.movieId ??
        movie.id;


    if (
        id === undefined ||
        id === null ||
        id === "" ||
        id === "undefined" ||
        id === "null"
    ) {

        return null;

    }


    const numericId =
        Number(id);


    if (
        !Number.isFinite(numericId)
    ) {

        return null;

    }


    return numericId;

}


// =====================================================
// NORMALIZE MOVIES
// =====================================================

function normalizeMovies(movies) {

    if (!Array.isArray(movies)) {

        return [];

    }


    return movies
        .map(function (movie) {

            const movieId =
                getMovieId(movie);


            if (movieId === null) {

                return null;

            }


            return {

                ...movie,

                movieId: movieId

            };

        })

        .filter(Boolean);

}


// =====================================================
// DISPLAY MOVIES IN GRID
// =====================================================

function displayMoviesInGrid(
    movies,
    grid
) {

    if (!grid) {

        return;

    }


    movies =
        normalizeMovies(movies);


    if (movies.length === 0) {

        grid.innerHTML = `

            <div class="no-results">

                No movies found.

            </div>

        `;

        return;

    }


    grid.innerHTML = "";


    movies.forEach(function (movie) {

        const card =
            createMovieCard(movie);


        if (card) {

            grid.appendChild(card);

        }

    });

}


// =====================================================
// DISPLAY SEARCH / GENRE RESULTS
// =====================================================

function displayMovies(
    movies,
    title,
    showResultsSection
) {

    let existing =
        document.getElementById(
            "dynamicResults"
        );


    if (!existing) {

        existing =
            document.createElement(
                "section"
            );

        existing.id =
            "dynamicResults";

        existing.className =
            "section";


        const main =
            document.querySelector("main");


        if (main) {

            main.prepend(existing);

        }

    }


    existing.innerHTML = `

        <div class="section-header">

            <div>

                <p class="section-label">
                    RESULTS
                </p>

                <h2>
                    ${escapeHtml(title)}
                </h2>

            </div>

        </div>


        <div
            class="movie-grid"
            id="dynamicMovieGrid"
        ></div>

    `;


    const grid =
        document.getElementById(
            "dynamicMovieGrid"
        );


    if (grid) {

        displayMoviesInGrid(
            movies,
            grid
        );

    }


    existing.scrollIntoView({
        behavior: "smooth"
    });

}


// =====================================================
// CREATE MOVIE CARD
// =====================================================

function createMovieCard(movie) {

    const movieId =
        getMovieId(movie);


    if (movieId === null) {

        console.warn(
            "Skipping movie with invalid ID:",
            movie
        );

        return null;

    }


    const card =
        document.createElement(
            "div"
        );


    card.className =
        "movie-card";


    const title =
        movie.title ||
        "Unknown Movie";


    const genres =
        movie.genres ||
        "Unknown";


    let rating =
        movie.rating;


    if (
        rating === undefined ||
        rating === null ||
        rating === "" ||
        rating === "nan"
    ) {

        rating = "N/A";

    }


    const poster =
        movie.poster || null;


    let posterHTML;


    if (poster) {

        posterHTML = `

            <img
                src="${escapeHtml(poster)}"
                alt="${escapeHtml(title)}"
                loading="lazy"
                onerror="
                    this.style.display='none';
                    this.parentElement.innerHTML='🎬';
                "
            >

        `;

    }

    else {

        posterHTML = "🎬";

    }


    card.innerHTML = `

        <div
            class="poster-placeholder"
            onclick="openMovieDetails(${movieId})"
        >

            ${posterHTML}

        </div>


        <div class="movie-info">

            <h3
                onclick="openMovieDetails(${movieId})"
                style="cursor:pointer;"
            >

                ${escapeHtml(title)}

            </h3>


            <p>

                ${escapeHtml(genres)}

            </p>


            <div class="movie-rating">

                ⭐ ${escapeHtml(
                    String(rating)
                )}

            </div>


            <div class="movie-actions">

                <button
                    class="favorite-button"
                    onclick="
                        event.stopPropagation();
                        addFavorite(${movieId});
                    "
                >

                    ❤️ Favorite

                </button>


                <button
                    class="favorite-button"
                    onclick="
                        event.stopPropagation();
                        addToWatchlist(${movieId});
                    "
                >

                    📌 Watchlist

                </button>

            </div>

        </div>

    `;


    return card;

}


// =====================================================
// OPEN MOVIE DETAILS
// =====================================================

function openMovieDetails(movieId) {

    const id =
        Number(movieId);


    if (!Number.isFinite(id)) {

        console.error(
            "Invalid movie ID:",
            movieId
        );

        return;

    }


    window.location.href =
        `/movie/${id}`;

}


// =====================================================
// ADD FAVORITE
// =====================================================

async function addFavorite(movieId) {

    try {

        const response =
            await fetch(
                "/api/favorites/add",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        movieId:
                            movieId

                    })

                }
            );


        const result =
            await response.json();


        if (result.success) {

            alert(
                "❤️ Movie added to favorites!"
            );

        }

        else {

            alert(
                result.message ||
                "Could not add movie."
            );

        }

    }

    catch (error) {

        console.error(
            "Favorite error:",
            error
        );

        alert(
            "Could not add movie to favorites."
        );

    }

}


// =====================================================
// ADD WATCHLIST
// =====================================================

async function addToWatchlist(movieId) {

    try {

        const response =
            await fetch(
                "/api/watchlist/add",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        movieId:
                            movieId

                    })

                }
            );


        const result =
            await response.json();


        if (result.success) {

            alert(
                "📌 Movie added to watchlist!"
            );

        }

        else {

            alert(
                result.message ||
                "Could not add movie."
            );

        }

    }

    catch (error) {

        console.error(
            "Watchlist error:",
            error
        );

        alert(
            "Could not add movie to watchlist."
        );

    }

}


// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHtml(value) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value ?? "";


    return div.innerHTML;

}
// =====================================================
// LOAD FAVORITES
// =====================================================

async function loadFavorites() {

    const grid =
        document.getElementById("favoritesGrid");

    if (!grid) {
        return;
    }

    try {

        const response =
            await fetch("/api/favorites");

        const movies =
            await response.json();

        if (!response.ok || !Array.isArray(movies)) {

            throw new Error(
                "Favorites request failed"
            );

        }

        if (movies.length === 0) {

            grid.innerHTML = `
                <p class="no-results">
                    No favorite movies yet.
                </p>
            `;

            return;
        }

        displayMoviesInGrid(
            movies,
            grid
        );

    }

    catch (error) {

        console.error(
            "Favorites loading error:",
            error
        );

        grid.innerHTML = `
            <p class="no-results">
                Could not load favorites.
            </p>
        `;

    }

}


// =====================================================
// LOAD WATCHLIST
// =====================================================

async function loadWatchlist() {

    const grid =
        document.getElementById("watchlistGrid");

    if (!grid) {
        return;
    }

    try {

        const response =
            await fetch("/api/watchlist");

        const movies =
            await response.json();

        if (!response.ok || !Array.isArray(movies)) {

            throw new Error(
                "Watchlist request failed"
            );

        }

        if (movies.length === 0) {

            grid.innerHTML = `
                <p class="no-results">
                    No movies in your watchlist yet.
                </p>
            `;

            return;
        }

        displayMoviesInGrid(
            movies,
            grid
        );

    }

    catch (error) {

        console.error(
            "Watchlist loading error:",
            error
        );

        grid.innerHTML = `
            <p class="no-results">
                Could not load watchlist.
            </p>
        `;

    }

}
// =====================================================
// LOAD FAVORITES
// =====================================================

async function loadFavorites() {

    const grid =
        document.getElementById("favoritesGrid");

    if (!grid) {
        return;
    }

    try {

        const response =
            await fetch("/api/favorites");

        const movies =
            await response.json();

        if (!response.ok || !Array.isArray(movies)) {
            throw new Error("Favorites request failed");
        }

        if (movies.length === 0) {

            grid.innerHTML = `
                <div class="no-results">
                    ❤️ No favorite movies yet.
                </div>
            `;

            return;
        }

        displayMoviesInGrid(
            movies,
            grid
        );

    }

    catch (error) {

        console.error(
            "Favorites error:",
            error
        );

        grid.innerHTML = `
            <div class="no-results">
                Could not load favorites.
            </div>
        `;

    }

}


// =====================================================
// LOAD WATCHLIST
// =====================================================

async function loadWatchlist() {

    const grid =
        document.getElementById("watchlistGrid");

    if (!grid) {
        return;
    }

    try {

        const response =
            await fetch("/api/watchlist");

        const movies =
            await response.json();

        if (!response.ok || !Array.isArray(movies)) {
            throw new Error("Watchlist request failed");
        }

        if (movies.length === 0) {

            grid.innerHTML = `
                <div class="no-results">
                    📌 No movies in your watchlist yet.
                </div>
            `;

            return;
        }

        displayMoviesInGrid(
            movies,
            grid
        );

    }

    catch (error) {

        console.error(
            "Watchlist error:",
            error
        );

        grid.innerHTML = `
            <div class="no-results">
                Could not load watchlist.
            </div>
        `;

    }

}