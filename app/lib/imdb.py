from bs4 import BeautifulSoup
import requests

def get_metacritic_movielist():
    session = requests.Session()
    url = ""
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
        movie['date']  = data.find('div', class_='clamp-details').get_text().split('|')[0].replace('\n','').strip()
        movies += [movie]
    return movies
