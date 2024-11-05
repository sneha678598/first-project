import unittest
from disaster_app.backend.app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_fetch_data(self):
        result = self.app.get('/fetch_data?location=ExampleLocation')
        self.assertEqual(result.status_code, 200)
        self.assertIn('temperature', result.data.decode('utf-8'))
        # Add more tests for other endpoints

if __name__ == '__main__':
    unittest.main()
