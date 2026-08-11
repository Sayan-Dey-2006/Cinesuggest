🎬 CineSuggest

CineSuggest is a Python-based movie recommendation web application that helps users search for movies, discover similar movies, explore top-rated movies, and manage their personal favorites and watchlist.

---

🚀 Features

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

🛠️ Technologies Used

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- Flask
- Pandas
- Requests

Database

- SQLite

API

- TMDB API

Recommendation System

- Content-based Movie Recommendation
- Cosine Similarity

---

📂 Project Structure

CineSuggest/
│
├── app.py
├── README.md
├── .gitignore
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

«🔐 The ".env" file is used locally for API credentials and is intentionally excluded from GitHub using ".gitignore".»

---

⚙️ Installation & Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd CineSuggest

2. Install dependencies

pip install -r requirements.txt

3. Create a ".env" file

Create a ".env" file in the project root and add your TMDB API key:

TMDB_API_KEY=your_api_key_here

⚠️ Never upload your real API key to GitHub.

4. Run the application

python app.py

Open the local URL displayed in the terminal.

---

🎯 Project Goal

The main goal of CineSuggest is to build a practical movie recommendation platform while learning and implementing:

- Python development
- Flask web development
- Frontend development
- REST APIs
- SQLite database management
- Content-based recommendation systems
- Cosine similarity
- Multithreading
- Git and GitHub

---

🔮 Future Improvements

- 🤖 AI-powered movie recommendations
- 👤 User authentication
- ❤️ Personalized recommendations
- 🌙 Dark mode
- ⭐ User reviews and ratings
- 🎞️ More detailed movie information
- 📱 Improved mobile responsiveness

---

👨‍💻 Developer

Sayan Dey

BCA Student | Python & Web Development Enthusiast

---

⭐ If you find this project useful, consider giving the repository a star!