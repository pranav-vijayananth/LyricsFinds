from bs4 import *
from requests_html import HTMLSession
import requests

session = HTMLSession()

query = input("Gimme query: ")
url = f"https://www.google.com/search?q={query} genius.com"
url = url.replace(' ', "%20")

search_page = session.get(url)
soup = BeautifulSoup(search_page.content, "html.parser")

results = soup.find('h3', class_='LC20lb DKV0Md')
results = results.span.contents[0]


results_list = results.split()
seperator = results_list.index('–')
lyrics_keyword = results_list.index('Lyrics')

artist_name = results_list[0:seperator]
song_name = results_list[seperator+1:lyrics_keyword]

print(artist_name)
print(song_name)