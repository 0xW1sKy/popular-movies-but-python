import requests
import json
import time
from urllib.parse import urlencode
from datetime import datetime, timedelta, date

def call_tmdb_api(apikey,uri):
    retry = True
    while retry:
        Authorization = "Bearer " + apikey
        headers = { 
            "Authorization": Authorization,
            "Content-Type": "application/json;charset=utf-8"
        }
        url = "http://api.themoviedb.org/3/{}".format(uri)
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            sleeptime = response.headers['retry-after'] * 1100
            return
        if response.status_code != 200:
            print("Warning: TMDB request failed: {}".format(response.status_code))
            return response
        output = json.loads(response.content.decode('utf-8'))
        retry = False
    return output

def find_tmdb_movie_by_imdbid(apikey,imdbId):
    uri = "find/{}?api_key={}&language=en-US&external_source=imdb_id".format(imdbId,apikey)            
    info = call_tmdb_api(apikey,uri)
    return info

def get_tmdb_popular_movie_query_string(page=1):
    year = timedelta(days=365)
    parms = {
        'sort_by': 'popularity.desc',
        'vote_count.gte': 25,
        'vote_average.gte': 4,
        'page': page,
        'language': 'en',
        'release_date.gte': (date.today()-(year*1.5)).isoformat(),
        'release_date.lte': (date.today()-(timedelta(days=30))).isoformat()
    }
    output = urlencode(parms)
    return output

def get_tmdb_popular_movies(apikey):
    page = 0
    total_pages = 1
    results = []
    while page <= total_pages:
        page += 1
        query_string = get_tmdb_popular_movie_query_string()
        uri = "discover/movie?api_key={}&{}".format(apikey,query_string)
        result = call_tmdb_api(apikey,uri)
        results += result['results']
        page = result['page']
        total_pages = result['total_pages']
    return results


def get_tmdb_movie(apikey,tmdbid):
    uri = "movie/{}?api_key={}".format(tmdbid, apikey)
    response = call_tmdb_api(apikey,uri)
    return response

def search_tmdb_movie(apikey,title,year):
    query = {
        "query": title.replace("/[^\w\s]/gi", ''),
        "year": year
    }
    query_string = urlencode(query)    
    uri = "search/movie?api_key={}&{}".format(apikey,query_string)
    response = call_tmdb_api(apikey,uri)
    return response
