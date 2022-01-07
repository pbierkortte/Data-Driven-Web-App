from flask import Flask, jsonify, render_template
import plotly.express as px
import pandas as pd
import pycountry

from src.crawler import Crawler, BitlyApiTokenNotSetError

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config['JSON_SORT_KEYS'] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/v1/avgDailyClicksByCountry")
def get_avg_daily_clicks_by_country():
    crawler = Crawler()
    avg_daily_clicks_by_country = crawler.avg_daily_clicks_by_country()
    return jsonify(avg_daily_clicks_by_country)

@app.route("/viz/ClicksByLocation")
def clicks_by_location():
    countries = [{"alpha_2": country.alpha_2, "alpha_3": country.alpha_3} for country in pycountry.countries]
    countries_df = pd.DataFrame(countries)

    data_df = pd.read_json(get_avg_daily_clicks_by_country().data)
    data_df = data_df.sort_values(by=["clicks", "country"])
    data_df["alpha_2"] = data_df["country"]
    data_df = data_df.merge(right=countries_df, how="inner", on="alpha_2")

    fig = px.choropleth(
        data_df
        , locations="alpha_3"
        , title="Clicks By Location Over Last 30 Days"
        , color="clicks"
        , labels={"clicks":"Avg. Daily Clicks", "country": "Location"}
    )
    return fig.to_html()

@app.errorhandler(404)
def page_not_found(error):
    return "This page does not exist", 404


@app.errorhandler(BitlyApiTokenNotSetError)
def bitly_api_token_not_set(error):
    return "Environment variable 'BITLY_API_TOKEN' is not set", 500
