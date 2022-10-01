# popular-movies-but-python

Rewrite of [Steven Lu's Popular Movies](https://github.com/sjlu/popular-movies) tool.
But its in python.
Also it looks at new movies that have come out on streaming platforms, not just ones that are being released in theaters.


## about

This tool makes a best guess at what popular movies are based on a series of heuristics from multiple websites. This then returns a list of movies with their posters and IMDB ID.

Popular movies are based on some general rules:

    Rating greater than the general sentiment of movies currently out
    Released less than a year ago
    At least 3 weeks old to generate a "stable" rating
    Does not consider tastes, categories or genres of movies

## License
[MIT](/LICENSE)