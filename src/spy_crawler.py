import json, os
from src.crawler import Crawler


class Spy(Crawler):
    def __init__(self):
        super().__init__()
        self._intercepted = []
        self._test_dir = "test_data"
        os.makedirs(self._test_dir, exist_ok=True)

    def get_data(self, url, params: dict) -> dict:
        response = self.session.get(url=url, params=params).json()

        self._intercepted.append(
            {
                "request": {
                    "url": url,
                    "params": params
                },
                "response": response
            }
        )
        return response

    def save_input_intercepted(self):
        file_path = f"{self._test_dir}/input_intercepted.json"
        with open(file_path, 'w') as outfile:
            json.dump(self._intercepted, outfile, indent=4, sort_keys=True)
        print(f"Saved file: \'{file_path}\'")

    def save_output_avg_daily_clicks_by_country(self):
        file_path = f"{self._test_dir}/output_avg_daily_clicks_by_country.json"
        output_avg_daily_clicks_by_country = self.avg_daily_clicks_by_country()
        with open(file_path, 'w') as outfile:
            json.dump(output_avg_daily_clicks_by_country, outfile, indent=4, sort_keys=True)
        print(f"Saved file: \'{file_path}\'")
