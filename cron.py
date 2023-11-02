import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_search_project.settings")
import django
django.setup()
import requests
from movie_search_app.models import Movie
from django.utils.timezone import now
import logging
from movie_search_app.tasks import logger

def fetch_and_save_tmdb_data():
    try:
        url = 'https://api.themoviedb.org/3/discover/movie'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1OWMyZmE2N2FmYjIyNTAwMWVkMTZjMzk1NDVmYTc0YyIsInN1YiI6IjY1MzQwYmQ0NDJkODM3MDBhY2UwZjQ0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DOoQ9hJQ1rjqxxOlyRmAx5IBvZMdUCiE_TW05CNl9rY',
            'accept': 'application/json',
        }
        page = 1  # Start with page 1
        all_movies = []

        while True:
            params = {
                'include_adult': 'false',
                'include_video': 'false',
                'language': 'en-US',
                'page': page,
                'sort_by': 'popularity.desc',
            }

            response = requests.get(url, headers=headers, params=params)
            logger.info(f"Task check poit api response")
            if response.status_code == 200:
                data = response.json().get('results', [])
                if not data:
                    break  # No more data to fetch
                for movie_data in data:
                    movie_obj = Movie.objects.filter(title=movie_data.get('title')).last()
                    if movie_obj:
                        pass
                    else:
                        try:
                            Movie.objects.create(title=movie_data.get('title', 'N/A'),
                                                 overview=movie_data.get('overview', 'No overview available'),
                                                 rating=movie_data.get('vote_average', 0.0),
                                                 release_date=movie_data.get('release_date', '1000-01-01'))
                            page += 1
                            logger.info(f"Movie {movie_data['title']} Saved")
                            print(f"Movie {movie_data['title']} Saved")
                        except:
                            pass
            else:
                logger.info(f"Failed to fetch data from TMDb API (page {page}): {response.status_code}")
                break

        print(f"Saved {len(all_movies)} movies at {now()}")
    except Exception as e:
        print(f'Execption occured {e}')


fetch_and_save_tmdb_data()
