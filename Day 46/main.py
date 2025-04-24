# ---------------------------- IMPORTS ------------------------------- #

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
from pprint import pprint  # For better visualization of the results
import re

# ---------------------------- CONFIG ------------------------------- #

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# ---------------------------- SPOTIPY AUTHENTICATION ------------------------------- #

def authenticate_spotify():
    """
    Authenticate with the Spotify API using the Spotipy library.
    Returns an authenticated Spotipy instance.
    """
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=["playlist-modify-private"]
    ))

# ---------------------------- BILLBOARD SCRAPING ------------------------------- #

def get_billboard_song_titles(date_input):
    """
    Scrape the Billboard Hot 100 chart for a specific date and return the song titles.
    """
    # Construct the URL for the Billboard Hot 100 chart of the given date
    url = f"https://www.billboard.com/charts/hot-100/{date_input}"

    # Set the headers to simulate a browser request (avoid blocking the request)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        song_titles = []
        
        for song in soup.find_all('span', class_="o-chart-results-list-row-container"):
            title = song.find('span', class_="o-chart-results-list-row-container__title")
            if title:
                song_titles.append(title.get_text(strip=True))

        if not song_titles:
            print(f"No songs were found for the week of {date_input}. Please check the date or the Billboard website.")
        
        return song_titles
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

# ---------------------------- SPOTIFY SONG SEARCH ------------------------------- #

def search_song_on_spotify(sp, song_name, year):
    """
    Search for a song on Spotify by name and year, returning its URI.
    """
    try:
        query = f"track:{song_name} year:{year}"
        result = sp.search(q=query, type="track", limit=1)

        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['uri']
            return track_uri
        else:
            print(f"Song '{song_name}' from the year {year} was not found on Spotify.")
            return None
    except Exception as e:
        print(f"Error searching for song '{song_name}': {e}")
        return None

# ---------------------------- PLAYLIST CREATION ------------------------------- #

def create_spotify_playlist(sp, user_id, date_input):
    """
    Create a new private playlist on Spotify with the name 'YYYY-MM-DD Billboard 100'.
    Returns the playlist ID.
    """
    playlist = sp.user_playlist_create(user_id, f"{date_input} Billboard 100", public=False)
    return playlist['id']

# ---------------------------- MAIN ------------------------------- #

def main():
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Get user info (to retrieve the user ID for playlist creation)
    user_info = sp.current_user()
    user_id = user_info['id']

    # Ask the user for the date of the Billboard Hot 100 chart with input validation
    while True:
        date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
        
        # Check if the input matches the YYYY-MM-DD format using a regex
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_input):
            break
        else:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

    # Get the song titles from Billboard
    song_titles = get_billboard_song_titles(date_input)

    # Print the song titles
    if song_titles:
        print(f"Top 100 songs for the week of {date_input}:")
        for index, title in enumerate(song_titles, start=1):
            print(f"{index}. {title}")

    # Search for each song on Spotify and collect the URIs
    spotify_uris = []
    for song in song_titles:
        song_year = date_input.split('-')[0]  # Extract the year from the input date
        track_uri = search_song_on_spotify(sp, song, song_year)

        if track_uri:
            spotify_uris.append(track_uri)

    # Pretty print the list of Spotify URIs
    pprint(spotify_uris)

    # Create the Spotify playlist
    if spotify_uris:
        playlist_id = create_spotify_playlist(sp, user_id, date_input)
        print(f"Created Playlist with ID: {playlist_id}")

        # Add the found tracks to the playlist
        sp.playlist_add_items(playlist_id, spotify_uris)
        print(f"Added {len(spotify_uris)} songs to the playlist.")
    else:
        print("No songs to add to the playlist.")

if __name__ == "__main__":
    main()
