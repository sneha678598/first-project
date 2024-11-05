# test_live_data_fetch.py

import unittest
from src.idms_functions import fetch_live_data

class TestLiveDataFetch(unittest.TestCase):
    def test_fetch_live_data(self):
        api_key = 'd3437b12773eb0feaeba59084f496eeb'
        city_name = 'London'
        api_url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = fetch_live_data(api_url)
        self.assertIsNotNone(response)
        self.assertIn('temperature', response)

if __name__ == '__main__':
    unittest.main()










