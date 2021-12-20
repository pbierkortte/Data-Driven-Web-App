import json
import unittest
from src.crawler import Crawler

file_input_intercepted = open("test_data/input_intercepted.json")
input_intercepted = json.load(file_input_intercepted)
file_input_intercepted.close()

file_daily_clicks_by_country = open("test_data/output_avg_daily_clicks_by_country.json")
expected_daily_clicks_by_country = json.load(file_daily_clicks_by_country)
file_daily_clicks_by_country.close()

class MockCrawler(Crawler):
    def __init__(self):
        super().__init__()

    def get_data(self, url, params:dict) -> dict:
        request = {
            "params": params,
            "url": url,
        }
        response = list(filter(lambda rec: str(rec["request"]) == str(request), input_intercepted))[0][
            "response"]
        return response

class TestCrawler(unittest.TestCase):
    def test_avg_daily_clicks_by_country(self):
        crawler = MockCrawler()

        result = crawler.avg_daily_clicks_by_country()

        self.assertEqual(result,expected_daily_clicks_by_country)

if __name__ == '__main__':
    unittest.main()
