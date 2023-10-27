from celery import shared_task, Celery
import requests
from celery.schedules import crontab
from movie_search_app.models import Movie
from django.utils.timezone import now
import logging
logging.basicConfig(
    filename='movie_update_task.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = Celery('your_app_name', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
app.conf.beat_schedule = {
    'fetch-tmdb-data-every-hour': {
        'task': 'movie_search_project.tasks.fetch_and_save_tmdb_data',
        'schedule': crontab(minute=1),
    },
}
app.conf.timezone = 'Asia/Kolkata'


@shared_task
def fetch_and_save_tmdb_data():
    print("2")
    try:
        logger.info(f"Cron job started")
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
                        Movie.objects.create(title=movie_data.get('title', 'N/A'), overview=movie_data.get('overview', 'No overview available'),
                                                     rating=movie_data.get('vote_average', 0.0),release_date=movie_data.get('release_date', '0000-00-00'))
                        page += 1
                        logger.info(f"Movie {movie_data['title']} Saved")
            else:
                logger.info(f"Failed to fetch data from TMDb API (page {page}): {response.status_code}")
                break

        logger.info(f"Saved {len(all_movies)} movies at {now()}")

    except Exception as e:
        logger.exception(f'Exception occurred: {e}')
