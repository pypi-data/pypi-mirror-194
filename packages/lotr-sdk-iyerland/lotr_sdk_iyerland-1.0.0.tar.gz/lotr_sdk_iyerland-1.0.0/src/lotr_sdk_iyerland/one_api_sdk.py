import json
import logging
import urllib3
from urllib3.util.retry import Retry
from urllib3.util.timeout import Timeout


def _get_logger(log_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def _get_retry_strategy():
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    return retry


def _get_timeout_strategy():
    timeout = Timeout(connect=2.0, read=10.0)
    return timeout


class OneApiSdk:
    """The OneApiSdk class which provides an abstraction to the Lord of the Rings API

    You would need to instantiate this class and pass it your access token (api key) and log level (defaults to DEBUG).
    """

    def __init__(self, api_key, log_level=logging.DEBUG):
        self.http = urllib3.PoolManager(retries=_get_retry_strategy(), timeout=_get_timeout_strategy())
        self.headers = {'Authorization': f'Bearer {api_key}'}
        self.base_url = 'https://the-one-api.dev/v2'
        self.logger = _get_logger(log_level)

    def _make_request(self, url):
        self.logger.debug(f'Making request to {url}')
        response = self.http.request('GET', url, headers=self.headers)
        if response.status != 200:
            raise Exception(f'Request failed with status {response.status}: {response.data.decode("utf-8")}')
        return json.loads(response.data.decode('utf-8'))

    def get_movies(self):
        """A function to retrieve all the movies from The Lord of the Rings"""
        url = f'{self.base_url}/movie'
        return self._make_request(url)

    def get_movie(self, movie_id):
        """A function to retrieve a movie given its id from The Lord of the Rings"""
        url = f'{self.base_url}/movie/{movie_id}'
        return self._make_request(url)

    def get_movie_quotes(self, movie_id):
        """A function to retrieve all the quotes given a movie_id from The Lord of the Rings"""
        url = f'{self.base_url}/movie/{movie_id}/quote'
        return self._make_request(url)
