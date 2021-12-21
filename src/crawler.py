import os
from requests import Session, request
from requests.structures import CaseInsensitiveDict
import pandas as pd


class BitlyApiTokenNotSetError(Exception):
    def __init__(self):
        self.message = "Environment variable BITLY_API_TOKEN is not set"
        super().__init__(self.message)


class Crawler:
    def __init__(self):
        self.session = Session()
        try:
            bitly_api_token = os.environ["BITLY_API_TOKEN"]
        except KeyError as e:
            raise BitlyApiTokenNotSetError() from e
        self.headers = CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"
        self.headers["Authorization"] = f"Bearer {bitly_api_token}"
        self.session.headers = self.headers

    def __del__(self):
        self.session.close()

    def get_data(self, url, params:dict) -> dict:
        response = self.session.get(url=url, params=params).json()
        return response

    def get_user_default_group(self) -> str:
        url = "https://api-ssl.bitly.com/v4/user"
        params = {}
        response = self.get_data(url=url, params=params)
        group_id = response["default_group_guid"]
        return group_id

    def get_links_by_group(self, group_id) -> list:
        def get_links_gen():
            params = {"size": 100}
            url = f"https://api-ssl.bitly.com/v4/groups/{group_id}/bitlinks"
            while url:
                response = self.get_data(url=url, params=params)
                for link in response["links"]:
                    yield link["id"]
                    url = response["pagination"]["next"]
        return list(get_links_gen())

    def get_link_metrics_by_country(self, link_id) -> list:
        params = {"unit": "day", "units": 30}
        url = f"https://api-ssl.bitly.com/v4/bitlinks/{link_id}/countries"
        response = self.get_data(url=url, params=params)
        metrics = []
        for country in response["metrics"]:
            metrics.append({
                "country": country["value"],
                "clicks": country["clicks"]
            })
        return metrics


    def avg_daily_clicks_by_country(self) -> list:
        g = self.get_user_default_group()
        links = self.get_links_by_group(g)
        metric_list = []
        for link in links:
            link_metrics = self.get_link_metrics_by_country(link)
            if len(link_metrics):
                for record in link_metrics:
                    metric_list.append(record)
        df = pd.DataFrame(metric_list).groupby(by=["country"], as_index=False).sum()
        df["clicks"] = df.clicks / 30
        df = df.sort_values(by='country')
        return df.to_dict('records')