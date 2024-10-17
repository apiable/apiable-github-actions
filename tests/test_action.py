import unittest
from unittest.mock import patch
import requests

class TestCustomGitHubAction(unittest.TestCase):
    @patch('requests.post')
    @patch('requests.get')
    def test_action(self, mock_get, mock_post):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '{"openapi": "3.0.0"}'
        
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"url": "https://apiable.s3.eu-central-1.amazonaws.com/public/dev/public/dev/test.json"}
        
        import action.main
        action.main.main()

if __name__ == '__main__':
    unittest.main()
