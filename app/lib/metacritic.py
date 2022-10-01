from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_metacritic_movielist():
    session = requests.Session()
    url = "https://www.metacritic.com/browse/movies/score/metascore/90day/filtered?sort=desc"
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    moviedata = soup.find_all('td', class_='clamp-summary-wrap')
    movies = []
    for data in moviedata:
        movie = {
            "score":"",
            "title":"",
            "date":""
        }
        movie['score'] = data.find('div', class_='metascore_w').get_text()
        movie['title'] = data.find('a', class_='title').get_text()  
        movie['date']  = datetime.strptime(data.find('div', class_='clamp-details').get_text().split('|')[0].replace('\n','').strip(), "%B %d, %Y").strftime("%Y-%m-%d")
        movies += [movie]
    return movies
