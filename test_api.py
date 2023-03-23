import unittest
from unittest.mock import patch, Mock
from main import app
import search_results_mock


class testSearchResults(unittest.TestCase):
    # to test for the flask client
    def setUp(self):
        self.app = app.test_client()

    @patch('main.requests.get')
    def test_search_results(self, mock_create):
        mock_response = Mock()
        mock_response.json.return_value = search_results_mock.mocked_api_data
        mock_create.return_value = mock_response

        # Make a request to the 'search_results' function with query term
        response_search = self.app.get('/search_results?term=python')

        self.assertEqual(response_search.status_code, 200)
        # Assert that the response contains the expected videos data
        self.assertIn(b'python Video1', response_search.data)
        self.assertIn(b'python Video2', response_search.data)


if __name__ == '__main__':
    unittest.main()
