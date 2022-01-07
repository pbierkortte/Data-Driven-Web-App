import unittest
import os
from multiprocessing import Process
from src.app import app
from requests import Session


class TestApp(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5000/"
        os.environ["FLASK_ENV"] = "testing"
        self.server = Process(target=app.run)
        self.server.start()
        self.server.join(2)
        self.session = Session()

    def test_server_returns_success(self):
        status_code = self.session.get(url=f"{self.host}").status_code
        self.assertEqual(status_code, 200)

    def test_avg_daily_clicks_by_country_returns_success(self):
        status_code = self.session.get(url=f"{self.host}api/v1/avgDailyClicksByCountry").status_code
        self.assertEqual(status_code, 200)

    def test_viz_clicks_by_location_returns_success(self):
        status_code = self.session.get(url=f"{self.host}viz/ClicksByLocation").status_code
        self.assertEqual(status_code, 200)

    def test_server_page_not_found_error(self):
        expected_content = b"This page does not exist"
        nonexistent_url = f"{self.host}pepper-night-census-polar-hero-chalk"
        response = self.session.get(url=nonexistent_url)
        status_code = response.status_code
        content = response.content
        self.assertEqual(status_code, 404)
        self.assertEqual(content, expected_content)

    def test_server_bitly_api_token_set(self):
        bitly_api_token = os.getenv("BITLY_API_TOKEN")
        self.assertNotEqual(bitly_api_token, "")

    def tearDown(self):
        self.session.close()
        self.server.kill()