# 🎬 Cinesuggest

Cinesuggest is a Python-based movie recommendation web application that helps users search for movies, discover similar movies, explore top-rated movies, and manage their personal favorites and watchlist.

---

## 🚀 Features

- 🔎 Movie Search
- 🤖 Movie Recommendation System
- ⭐ Top Rated Movies
- 🎭 Genre-based Movie Discovery
- 🎬 Movie Details
- 🖼️ Dynamic Movie Posters
- ⭐ Movie Ratings
- ❤️ Favorites
- 📌 Watchlist
- ⚡ Fast movie loading using multithreading
- 💾 Database-based Favorites and Watchlist
- 🌐 Flask Web Application

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Pandas
- Requests

### Database
- SQLite

### APIs
- TMDB API

### Machine Learning / Recommendation
- Cosine Similarity
- Content-based Movie Recommendation

---

## 📂 Project Structure

```text
Cinesuggest/
│
├── app.py
├── .env
├── README.md
│
├── backend/
│   ├── movie_loader.py
│   ├── recommender.py
│   └── similarity.py
│
├── database/
│   ├── database.py
│   └── models.py
│
├── templates/
│   ├── index.html
│   ├── favorites.html
│   ├── watchlist.html
│   └── movie_details.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
└── data/
    ├── movies.csv
    ├── links.csv
    └── ratings.csv