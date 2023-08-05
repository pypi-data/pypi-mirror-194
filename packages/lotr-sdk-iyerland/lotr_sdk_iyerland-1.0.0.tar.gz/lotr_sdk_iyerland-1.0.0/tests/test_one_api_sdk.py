import logging
import unittest
from src.lotr_sdk_iyerland.one_api_sdk import OneApiSdk


class TestOneApiSdk(unittest.TestCase):
    def setUp(self):
        self.api_key = 'IiIuEVn9PSxzisgJRgHV'
        self.one_api_sdk = OneApiSdk(self.api_key, log_level=logging.DEBUG)

    def test_get_movies(self):
        movies = self.one_api_sdk.get_movies()
        movies_docs = movies['docs']
        self.assertIsInstance(movies_docs, list)
        self.assertEqual(len(movies_docs), 8)

    def test_get_movie(self):
        movie_id = '5cd95395de30eff6ebccde5c'
        movie = self.one_api_sdk.get_movie(movie_id)
        movie_docs = movie['docs']
        movie_details = movie_docs[0]
        self.assertIsInstance(movie_details, dict)
        self.assertEqual(movie_details['_id'], movie_id)
        self.assertEqual(movie_details['name'], "The Fellowship of the Ring")

    def test_get_movie_quotes(self):
        movie_id = '5cd95395de30eff6ebccde5c'
        movie_quotes = self.one_api_sdk.get_movie_quotes(movie_id)
        movie_quotes_docs = movie_quotes['docs']
        movie_quote_first = movie_quotes_docs[0]
        self.assertIsInstance(movie_quotes['docs'], list)
        self.assertEqual(movie_quote_first['_id'], '5cd96e05de30eff6ebcced61')
        self.assertEqual(movie_quote_first['dialog'], 'Who is she? This woman you sing of?')



if __name__ == '__main__':
    unittest.main()
