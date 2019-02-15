import omdb_api

app = omdb_api.MovieSearchOMDB()


def main():
    v = 'Hello'

    while v:
        print('Movie DB Search.')
        v = input('Search for [m]ovies, [s]eries or [e]nter a title: ')

        if v == 'm':
            search_movie()
        elif v == 's':
            search_series()
        elif v == 'e':
            item_search()

    print("Goodbye.")


def search_movie():
    title = input('Enter movie keyword: ')
    response = app.movie_search(title)
    movies = response.json()

    if movies["Response"] == "True":

        results = int(movies['totalResults'])//10 + 1

        num = 1
        ids = {}

        for p in range(1, int(results)+1):
            response = app.movie_search(title, p)
            movies = response.json()

            for i in movies['Search']:
                ids[num] = i.get('imdbID')
                print(f"{num}. {i.get('Title')}, {i.get('Year')} IMDB Code: {ids[num]}")
                num += 1

        print()
        print(f"{movies['totalResults']} results retrieved.")
        print()

        id_ = int(input("Enter movie number to check: "))
        response = app.code_search(ids[id_])

        movie = response.json()

        print()
        print(f'Details for selected movie: {movie.get("imdbID")}')
        print(f"Title: {movie.get('Title')}")
        print(f"Plot: {movie.get('Plot')}")
        print(f"Casts: {movie.get('Actors')}")
        print(f"Movie Length: {movie.get('Runtime')}")
        print(f"Rated: {movie.get('Rated')}")
        print(f"Release Date: {movie.get('Released')}")
        print(f"IMDB Score: {movie.get('imdb_score')}")
        print()

    else:
        print("No movies found with chosen keyword.")
        print()


def search_series():
    title = input('Enter series title: ')
    response = app.series_search(title)
    series = response.json()

    if series["Response"] == "True":

        results = int(series['totalResults'])//10 + 1

        num = 1
        ids = {}

        for p in range(1, int(results)+1):
            response = app.series_search(title, p)
            series = response.json()

            for i in series['Search']:
                print(f"{num}. {i.get('Title')}, {i.get('Year')} IMDB Code: {ids[num]}")
                ids[num] = i.get('imdbID')
                num += 1

        print()
        print(f"{series['totalResults']} results retrieved.")
        print()

        id_ = int(input("Enter series number to check: "))
        response = app.code_search(ids[id_])

        series = response.json()

        print()
        print(f'Details for selected series: {series.get("imdbID")}')
        print(f"Title: {series.get('Title')}")
        print(f"Plot: {series.get('Plot')}")
        print(f"Casts: {series.get('Actors')}")
        print(f"Episode Length: {series.get('Runtime')}")
        print(f"Rated: {series.get('Rated')}")
        print(f"Number of Seasons: {series.get('totalSeasons')}")
        print(f"IMDB Score: {series.get('imdb_score')}")
        print()

    else:
        print("No movies found with chosen keyword.")
        print()


def item_search():
    title = input("Enter title: ")
    response = app.title_search(title)
    show = response.json()

    print()
    print(f'Details for selected series: {show.get("imdbID")}')
    print(f"Title: {show.get('Title')}")
    print(f"Plot: {show.get('Plot')}")
    print(f"Casts: {show.get('Actors')}")
    print(f"Genre: {show.get('Genre')}")
    print(f"{'Episode' if show.get('Type') == 'series' else  'Movie'} Length: {show.get('Runtime')}")
    print(f"Rated: {show.get('Rated')}")
    if show.get('Type') == 'series':
        print(f"Number of Seasons: {show.get('totalSeasons')}")
    print(f"IMDB Score: {show.get('imdbRating')}")
    print()


if __name__ == '__main__':
    main()
