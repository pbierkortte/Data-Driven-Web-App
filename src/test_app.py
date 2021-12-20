import unittest
import os
from multiprocessing import Process
from src.app import app
from requests import Session


class TestCrawler(unittest.TestCase):
    def setUp(self):
        os.environ["FLASK_ENV"] = "testing"
        self.server = Process(target=app.run)
        self.server.start()
        self.server.join(2)
        self.session = Session()

    def test_server_returns_success(self):
        status_code = self.session.get(url=f"http://127.0.0.1:5000/").status_code
        self.assertEqual(status_code,200)


    def test_avg_daily_clicks_by_country_returns_success(self):
        status_code = self.session.get(url=f"http://127.0.0.1:5000/api/v1/avgDailyClicksByCountry").status_code
        self.assertEqual(status_code,200)

    def tearDown(self):
        self.session.close()
        self.server.terminate()

