"""_summary_
Api tests
checks if a video title is in the response data
"""
import unittest
from unittest.mock import patch, Mock
from main import app
import search_results_mock


class TestSearchResults(unittest.TestCase):
    """_summary_
        this class uses the unittest framework
        its purpose is to generate search results
    """
    # to test for the flask client

    def setUp(self):
        self.app = app.test_client()

    @patch('main.requests.get')
    def test_search_results(self, mock_create):
        """_summary_
        in this function the test method is patching the 'requests.get' method
        in the main module. 
        """
        mock_response = Mock()
        mock_response.json.return_value = search_results_mock.mocked_api_data
        mock_create.return_value = mock_response

        # Make a request to the 'search_results' function with query term
        response_search = self.app.get('/search_results?term=python')

        # Assert that the response contains the expected videos data
        self.assertEqual(response_search.status_code, 200)
        self.assertIn(b'python Video1', response_search.data)
        self.assertIn(b'python Video2', response_search.data)


if __name__ == '__main__':
    unittest.main()
