import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/'

# Send a GET request to fetch the webpage content
response = requests.get(url)
webpage_html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage_html, 'html.parser')

# Extract movie titles using the HTML tag and class name
movies = soup.find_all('h3', class_='title')

# Create a list of movie titles and reverse their order (from rank 1 to 100)
movie_titles = [movie.getText() for movie in movies][::-1]

# Save the titles into a file named 'movies.txt'
with open('movies.txt', 'w', encoding='utf-8') as file:
    for title in movie_titles:
        file.write(title + '\n')

print("Movie titles have been successfully saved to 'movies.txt'.")
