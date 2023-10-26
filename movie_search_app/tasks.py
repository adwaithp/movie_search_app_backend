# your_app/management/commands/fetch_tmdb_data.py
from celery import shared_task
import requests
from movie_search_app.models import Movie
from django.utils.timezone import now
import logging
logging.basicConfig(
    filename='movie_update_task.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@shared_task
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

            if response.status_code == 200:
                data = response.json().get('results', [])
                if not data:
                    break  # No more data to fetch
                for movie in data:
                    movie = Movie.objects.all().last()
                    movie.title = movie['title']
                    movie.overview = movie['overview']
                    movie.rating = movie['vote_average']
                    movie.release_date = movie['release_date'] if movie['release_date'] else '0000-00-00'
                    movie.save()
                    page += 1
            else:
                print(f"Failed to fetch data from TMDb API (page {page}): {response.status_code}")
                break

        logger.info(f"Saved {len(all_movies)} movies at {now()}")

    except Exception as e:
        logger.exception(f'Exception occurred: {e}')
