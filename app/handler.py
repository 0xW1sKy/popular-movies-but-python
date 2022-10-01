from lib import imdb,metacritic,omdb,tmdb
from datetime import date, datetime, timedelta
import os
tmdbapikey = os.environ['tmdbapikey']
omdbapikey = os.environ['omdbapikey']

def filter_for_export(movielist):
    output = []
    for movie in movielist:
        item = {
            "title": movie['title'],
            "imdb_id": movie['imdbid'],
            "poster_url": movie['poster']
        }
        output += [item]
    return output    

def filter_by_release_date(movies):
    year = timedelta(days=365)
    tooold = datetime.fromisoformat((date.today()-(year*2)).isoformat())
    toonew = datetime.fromisoformat((date.today()-(timedelta(days=7))).isoformat())
    filteredlist = list(filter(lambda x: (tooold >= datetime.fromisoformat(x['release_date']) <= toonew ), movies))
    return filteredlist

def filter_by_popularity(movies):
    filteredlist = list(filter(lambda x: (x['popularity'] >= 10.0 ) , movies))
    return filteredlist

def get_movie_list(tmdbapikey):
    movielist = []
    mclist = metacritic.get_metacritic_movielist()
    for movie in mclist:
        title = movie['title']
        year = date.fromisoformat(movie['date']).year
        metacriticscore = movie['score']
        movieinfo = tmdb.search_tmdb_movie(tmdbapikey,title,year)
        if movieinfo['results']:
            tmdbid = movieinfo['results'][0]['id']
            moviedetail = tmdb.get_tmdb_movie(tmdbapikey,tmdbid)
            release_date = moviedetail['release_date']
            imdbid = moviedetail['imdb_id']
            popularity = moviedetail['popularity']
            poster_path = "https://image.tmdb.org/t/p/w500{}".format(moviedetail['poster_path'])
            output = {
                "title": title,
                "year": year,
                "metacritic_score": metacriticscore,
                "imdbid": imdbid,
                "tmdbid": tmdbid,
                "release_date": release_date,
                "popularity": popularity,
                "poster": poster_path
            }
            movielist += [output]
    return movielist

def handler(event, context):
    movielist = get_movie_list(tmdbapikey)
    movielist = filter_by_release_date(movielist)
    movielist = filter_by_popularity(movielist)
    movielist = filter_for_export(movielist)
    return movielist

#handler(0,0)