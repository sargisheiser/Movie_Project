"""
Movie CLI Application with user profiles (SQLAlchemy storage).
"""

import random
import difflib
import requests
import os
from dotenv import load_dotenv
from movies_storage import movie_storage_sql as storage
from movies_storage import user_storage_sql as user_storage

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/"


def command_list_movies(user_id, username):
   """Retrieve and display all movies for a user."""
   movies = storage.list_movies(user_id)
   if not movies:
       print(f"\n📢 {username}, your movie collection is empty.")
       return

   print(f"\n🎬 {username}, you have {len(movies)} movies in total:")
   for title, data in sorted(movies.items(), key=lambda x: x[0].casefold()):
       print(f"{title} ({data['year']}): {data['rating']:.1f}")


def command_add_movie(user_id):
   """Add a movie using OMDb API."""
   title = input("Enter movie title: ").strip()

   try:
       response = requests.get(OMDB_URL, params={"t": title, "apikey": API_KEY})
       response.raise_for_status()
   except requests.RequestException as e:
       print("Error: Could not connect to OMDb API.")
       print(e)
       return

   data = response.json()

   if data.get("Response") == "False":
       print(f"Movie '{title}' not found in OMDb.")
       return

   year = int(data.get("Year", 0))
   rating = float(data.get("imdbRating", 0.0)) if data.get("imdbRating") != "N/A" else 0.0
   poster = data.get("Poster", "")

   imdb_id = data.get("imdbID", "")
   country = data.get("Country", "Unknown")

   LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

   try:
       search = requests.get(
           "http://ws.audioscrobbler.com/2.0/",
           params={
               "method": "track.search",
               "track": f"{title} soundtrack",
               "api_key": lastfm_api,
               "format": "json",
               "limit": 1
           }
       ).json()
       soundtrack_url = search["results"]["trackmatches"]["track"][0]["url"]
   except Exception:
       soundtrack_url = None

   storage.add_movie(
       user_id,
       data["Title"],
       year,
       rating,
       poster,
       imdb_id,
       country,
       soundtrack_url
   )


def command_delete_movie(user_id):
   """Delete a movie for a user."""
   title = input("Enter movie title to delete: ").strip()
   storage.delete_movie(title, user_id)


def command_update_movie(user_id):
   """Prompt user for a movie and add/update a note."""
   title = input("Enter movie title to update: ").strip()
   note = input("Enter movie note: ").strip()
   storage.update_movie_note(user_id, title, note)


def command_statistics(user_id, username):
   """Show stats for a user's movies."""
   movies = storage.list_movies(user_id)
   if not movies:
       print(f"\n{username}, your collection is empty.")
       return

   ratings = [data["rating"] for data in movies.values()]
   avg = sum(ratings) / len(ratings)
   print(f"Average rating: {avg:.2f}")

   sorted_ratings = sorted(ratings)
   n = len(sorted_ratings)
   median = sorted_ratings[n // 2] if n % 2 else (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
   print(f"Median rating: {median:.2f}")

   max_rating = max(ratings)
   min_rating = min(ratings)

   print("\nBest movies:")
   for title, data in movies.items():
       if data["rating"] == max_rating:
           print(f"{title} ({data['year']}): {data['rating']}")


   print("\nWorst movies:")
   for title, data in movies.items():
       if data["rating"] == min_rating:
           print(f"{title} ({data['year']}): {data['rating']}")


def command_random_movie(user_id):
   """Pick a random movie from a user's collection."""
   movies = storage.list_movies(user_id)
   if not movies:
       print("No movies found.")
       return
   title = random.choice(list(movies.keys()))
   rating = movies[title]["rating"]
   print(f"Your random movie is: {title} with rating {rating:.1f}")


def command_search_movie(user_id):
   """Search a user's movies by keyword."""
   keyword = input("Enter keyword to search: ").strip().lower()
   movies = storage.list_movies(user_id)
   results = [(t, d) for t, d in movies.items() if keyword in t.lower()]


   if results:
       print("Search results:")
       for title, data in sorted(results, key=lambda x: x[0].casefold()):
           print(f"{title} ({data['year']}): {data['rating']}")
   else:
       print(f"The movie '{keyword}' does not exist.")
       suggestions = difflib.get_close_matches(keyword, movies.keys(), n=3, cutoff=0.4)
       if suggestions:
           print("Did you mean:")
           for s in suggestions:
               print(s)


def command_sort_by_rating(user_id):
   """Sort a user's movies by rating."""
   movies = storage.list_movies(user_id)
   if not movies:
       print("No movies found.")
       return
   sorted_movies = sorted(movies.items(), key=lambda x: (-x[1]["rating"], x[0].casefold()))
   print("Movies sorted by rating:")
   for title, data in sorted_movies:
       print(f"{title} ({data['year']}): {data['rating']}")


def command_sort_by_year(user_id):
   """Sort a user's movies by year."""
   movies = storage.list_movies(user_id)
   if not movies:
       print("No movies found.")
       return
   sorted_movies = sorted(movies.items(), key=lambda x: x[1]["year"], reverse=True)
   print("Movies sorted by year:")
   for title, data in sorted_movies:
       print(f"{title} ({data['year']}): {data['rating']}")


def command_filter_movies(user_id):
   """Filter a user's movies."""
   min_rating = input("Enter minimum rating (or leave blank): ").strip()
   start_year = input("Enter start year (or leave blank): ").strip()
   end_year = input("Enter end year (or leave blank): ").strip()

   min_rating = float(min_rating) if min_rating else None
   start_year = int(start_year) if start_year else None
   end_year = int(end_year) if end_year else None

   movies = storage.list_movies(user_id)
   filtered = []
   for title, data in movies.items():
       year, rating = data["year"], data["rating"]
       if min_rating is not None and rating < min_rating:
           continue
       if start_year is not None and year < start_year:
           continue
       if end_year is not None and year > end_year:
           continue
       filtered.append((title, year, rating))

   if not filtered:
       print("No movies found with the given filters.")
       return

   print("Filtered movies:")
   for title, year, rating in sorted(filtered, key=lambda x: (x[1], -x[2], x[0])):
       print(f"{title} ({year}): {rating}")


def country_to_flag(country_name: str) -> str:
   country = country_name.split(",")[0].strip()

   mapping = {
       "USA": "US",
       "United States": "US",
       "UK": "GB",
       "United Kingdom": "GB",
       "France": "FR",
       "Germany": "DE",
       "Italy": "IT",
       "Canada": "CA",
       "India": "IN",
       "Japan": "JP",
       "China": "CN"
   }

   code = mapping.get(country, None)
   if not code:
       return "🏳️"

   return "".join(chr(ord(c) + 127397) for c in code.upper())



def command_generate_website(user_id, username):
   movies = storage.list_movies(user_id)
   if not movies:
       print("No movies to display in website.")
       return

   with open("_static/index_template.html", "r", encoding="utf-8") as f:
       template = f.read()

   movie_items = []
   for title, data in movies.items():
       poster = data.get("poster") or ""
       year = data.get("year", "")
       note = data.get("note") or ""
       imdb_id = data.get("imdb_id", "")
       imdb_link = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else "#"
       country = data.get("country", "Unknown")
       flag = country_to_flag(country)
       movie_items.append(f"""
       <li>
           <div class="movie">
               <a href="{imdb_link}" target="_blank">
                   <img class="movie-poster" src="{poster}" alt="{title} poster" title="{data.get('note', '')}"/>
               </a>
           <div class="movie-title">{title} {flag}</div>
               <div class="movie-year">{year}</div>
               <div class="movie-rating">⭐ {data.get("rating", "N/A")}</div>
               {"<a class='soundtrack' href='" + data.get("soundtrack_url", "") + "' target='_blank'>🎵 Soundtrack</a>" if data.get("soundtrack_url") else ""}


           </div>
       </li>
       """)

   movie_grid = "\n".join(movie_items)


   output_html = template.replace("TEMPLATE_TITLE", f"{username}'s Movie App") \
                         .replace("TEMPLATE_MOVIE_GRID", movie_grid)

   with open(f"{username}.html", "w", encoding="utf-8") as f:
       f.write(output_html)

   print(f"Website for {username} was generated successfully.")


def print_menu(username):
   """Display menu options."""
   print(f"\n****** {username}'s Movie Database ******")
   print("0. Exit")
   print("1. List Movies")
   print("2. Add Movie")
   print("3. Delete Movie")
   print("4. Update Movie")
   print("5. Stats")
   print("6. Random Movie")
   print("7. Search Movie")
   print("8. Movies sorted by rating")
   print("9. Movies sorted by year")
   print("10. Filter Movies")
   print("11. Generate Website")
   print("12. Switch User")


def main():
   """Run the CLI main loop."""
   user_id, username = user_storage.select_user()
   print(f"\nWelcome back, {username}! 🎬")

   while True:
       print_menu(username)
       choice = input("Enter your choice: ").strip()

       if choice == "0":
           print("Bye!")
           break
       elif choice == "1":
           command_list_movies(user_id, username)
       elif choice == "2":
           command_add_movie(user_id)
       elif choice == "3":
           command_delete_movie(user_id)
       elif choice == "4":
           command_update_movie(user_id)
       elif choice == "5":
           command_statistics(user_id, username)
       elif choice == "6":
           command_random_movie(user_id)
       elif choice == "7":
           command_search_movie(user_id)
       elif choice == "8":
           command_sort_by_rating(user_id)
       elif choice == "9":
           command_sort_by_year(user_id)
       elif choice == "10":
           command_filter_movies(user_id)
       elif choice == "11":
           command_generate_website(user_id, username)
       elif choice == "12":
           user_id, username = user_storage.select_user()
           print(f"\nWelcome back, {username}! 🎬")
       else:
           print("Invalid choice. Please try again.")


if __name__ == "__main__":
   main()