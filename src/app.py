from flask import Flask, jsonify, render_template

from src.crawler import Crawler

app = Flask(__name__, template_folder="../templates",static_folder="../static")
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/api/v1/avgDailyClicksByCountry")
def get_avg_daily_clicks_by_country():
    crawler = Crawler()
    avg_daily_clicks_by_country = crawler.avg_daily_clicks_by_country()
    return jsonify(avg_daily_clicks_by_country)