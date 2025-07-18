from datetime import datetime

import pandas as pd
from imdb import IMDb


def get_imdb_url(movies_df):
    ia = IMDb()

    manual_links = {
        "65": "https://www.imdb.com/title/tt12261776/reviews/?ref_=tt_ururv_sm&sort=submission_date%2Casc"
    }

    movie_ids = []
    release_dates = []
    movie_titles = []
    imdb_review_urls = []

    review_sort_suffix = 'reviews/?ref_=tt_ql_2&sort=submission_date%2Casc'

    total_num_movies = movies_df.movie_id.max() + 1

    for index, row in movies_df.iterrows():
        print(f'\n========= Processing movie: {index+1}/{total_num_movies} ==========')
        movie_id = row['movie_id']
        movie_title = row['movie_title']
        release_date = datetime.strptime(row['release_date'], "%Y/%m/%d")
        release_year = release_date.year

        print(f'         Title: {movie_title} ({release_year})')

        # Search for the movie on IMDb
        if movie_title in manual_links:
            movie_url = manual_links[movie_title]
            print(f"Using manual IMDb review URL for '{movie_title}'")
        else:
            try:
                search_results = ia.search_movie(movie_title)
            except Exception as e:
                print(f"Error searching IMDb for '{movie_title}': {e}")
                continue

            if not search_results:
                print(f"Movie '{movie_title}' not found.")
                continue

            matched_movie = None
            for result in search_results:
                ia.update(result)
                if result.get('year') == release_year:
                    print(f"Trying match: {result.get('title')} ({result.get('year')})")
                    matched_movie = result
                    break

            if not matched_movie:
                print(f"No IMDb match found for {movie_title} ({release_year})")
                continue

            # Get IMDb URL for the matched movie
            movie = ia.get_movie(matched_movie.movieID)
            base_url = ia.get_imdbURL(movie)
            movie_url = base_url + review_sort_suffix

        # Store data
        movie_ids.append(movie_id)
        release_dates.append(release_date.strftime("%Y/%m/%d"))
        movie_titles.append(movie_title)
        imdb_review_urls.append(movie_url)

    movie_urls = pd.DataFrame({
        'movie_id': movie_ids,
        'movie_title': movie_titles,
        'release_date': release_dates,
        'imdb_review_url': imdb_review_urls
    })

    # save_path = "../data/imdb_review_urls.csv"
    # movie_urls.to_csv(save_path, index=False)

    return movie_urls