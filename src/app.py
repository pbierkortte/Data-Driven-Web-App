from flask import Flask, jsonify, render_template

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


@app.errorhandler(404)
def page_not_found(error):
    return "This page does not exist", 404


@app.errorhandler(BitlyApiTokenNotSetError)
def bitly_api_token_not_set(error):
    return "Environment variable 'BITLY_API_TOKEN' is not set", 500
