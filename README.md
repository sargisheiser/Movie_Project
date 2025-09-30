🎬 Movie App

A command-line and web-based movie manager where multiple users can store, organize, and view their personal movie collections.
Movies are fetched from the OMDb API, and additional metadata like soundtracks (Last.fm API), notes, IMDB links, and country flags are included.
A simple website is generated for each user with a clean movie grid.

✨ Features

👤 User Profiles – Each user has their own separate movie collection.

➕ Add Movies – Fetch details automatically from the OMDb API
.

🗑 Delete Movies – Remove movies from your collection.

📝 Update Notes – Add personal notes to each movie.

⭐ Ratings – Store and display IMDB ratings.

🌍 Country Flags – Show the origin country flag for each movie.

🔗 IMDB Links – Clicking a movie poster opens its IMDB page.

🎵 Soundtracks – Links to official soundtracks via Last.fm.

📊 Statistics – View average and median ratings, best/worst movies.

🔍 Search & Filter – Find movies by title, rating, or year.

🎲 Random Movie Picker – Can’t decide? Let the app choose for you.

🌐 Website Generator – Export a responsive HTML page of your collection.

📂 Project Structure
movie-project/
│── _static/
│   ├── index_template.html   # HTML template for generated site
│   ├── style.css             # CSS for website styling
│
│── data/
│   └── movies.db             # SQLite database
│
│── movies_storage/
│   ├── init.py
│   ├── movie_storage_sql.py  # Movie storage logic (SQLAlchemy)
│   └── user_storage_sql.py   # User storage logic
│
│── venv/                     # Virtual environment (ignored in git)
│── main.py                   # CLI entrypoint
│── README.md                 # Project documentation
│── requirements.txt          # Python dependencies
│── .gitignore                # Ignored files/folders

⚙️ Installation

Clone this repo:

git clone https://github.com/your-username/movie-app.git
cd movie-app


Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

🚀 Usage

Start the app:

python3 main.py

Example workflow
Welcome to the Movie App! 🎬
Select a user:
1. John
2. Sara
3. Create new user

Enter choice: 1
Welcome back, John! 🎬

** John's Movie Database **
0. Exit
1. List Movies
2. Add Movie
3. Delete Movie
4. Update Movie
...


Generate website:

Enter choice: 11
Website for John was generated successfully.


Then open John.html in your browser.

🔑 API Keys

OMDb API → Get free key

Last.fm API → Get key

Place them inside main.py:

API_KEY = "your-omdb-api-key"
LASTFM_API = "your-lastfm-api-key"

📸 Website Example

Movies are displayed in a grid with:

🎬 Poster (clickable → IMDB page)

⭐ Rating

📝 Hover note

🌍 Flag for country

🎵 Soundtrack link

🛠️ Tech Stack

Python 3.10+

SQLite + SQLAlchemy

Requests (for API calls)

HTML/CSS (for website)

📌 Roadmap / Bonus Features

🎨 Improve website styling (responsive grid for >20 movies)

🎧 Add embedded soundtrack player

🔥 Add favorite/liked movies toggle

📱 Export as PWA/mobile app

🤝 Contributing

Pull requests welcome! Feel free to fork this repo and open an issue for feature suggestions.

📜 License

MIT License © 2025 Sargis Heiser