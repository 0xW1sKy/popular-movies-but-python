import requests
import json

def get_omdb_info(apikey,imdbId):
    url = "http://www.omdbapi.com/?i={}&apikey={}".format(imdbId,apikey)
    response = requests.get(url)
    if response.status_code != 200:
        print("Warning: OMDB request failed: {}".format(response.status_code))
        return response.status_code
    return json.loads(response.content.decode('utf-8'))
