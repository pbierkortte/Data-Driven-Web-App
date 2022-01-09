import unittest
import os
from multiprocessing import Process
from src.app import app
from requests import Session

HOST = "127.0.0.1"
PORT = 9001

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = Process(target=app.run, kwargs=dict(port=PORT))
        cls.server.start()
    
    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
    
    def test_server_bitly_api_token_set(self):
        bitly_api_token = os.getenv("BITLY_API_TOKEN")
        self.assertNotEqual(bitly_api_token, "")
        
    def test_server_returns_success(self):
        url = f"http://{HOST}:{PORT}/"
        with Session() as session:
            response = session.get(url=url)
        self.assertEqual(response.status_code, 200)

    def test_avg_daily_clicks_by_country_returns_success(self):
        url = f"http://{HOST}:{PORT}/api/v1/avgDailyClicksByCountry"
        with Session() as session:
            response = session.get(url=url)
        self.assertEqual(response.status_code, 200)

    def test_viz_clicks_by_location_returns_success(self):
        url = f"http://{HOST}:{PORT}/viz/ClicksByLocation"
        with Session() as session:
            response = session.get(url=url)
        self.assertEqual(response.status_code, 200)

    def test_server_page_not_found_error(self):
        nonexistent_url = f"http://{HOST}:{PORT}/pepper-night-census-polar-hero-chalk"
        expected_content = b"This page does not exist"
        with Session() as session:
            response = session.get(url=nonexistent_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, expected_content)
