import requests
from bs4 import BeautifulSoup
import pandas as pd

start = "https://en.wikipedia.org/wiki/Billboard_year-end_top_singles_of_1946"

resp = requests.get(start)

bs = BeautifulSoup(resp.text, 'html.parser')
linksComponents = bs.select('.nowraplinks a')

links = ["/wiki/Billboard_year-end_top_singles_of_1946"]

for i in range(7, len(linksComponents)):
    links.append(linksComponents[i].get('href'))

songs = []
year = 1945

for link in links:
    year += 1
    resp = requests.get("https://en.wikipedia.org" + link)
    if (resp.status_code != 200):
        print(f"On link {link} status code: {resp.status_code}")
        continue
    print(f"On link: {link}")
    bs = BeautifulSoup(resp.text, 'html.parser')
    lines = bs.select('.wikitable tbody tr')
    for line in lines:
        song = [year]
        parts = line.select('td')
        for part in parts:
            a = part.select_one('a')
            if a != None:
                song.append(a.text)
            else:
                song.append(part.text)
        songs.append(song)
    print(f"Len of songs: {len(songs)}")

df = pd.DataFrame(data=songs, columns=['year', 'rank', 'title', 'artist'])
df.to_csv('songs.csv')