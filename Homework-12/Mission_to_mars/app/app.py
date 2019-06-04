from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_facts = mongo.db.mars_facts.find_one()
    return render_template("index.html", mars_facts=mars_facts)

@app.route("/scrape")
def scraper():
    mars_facts = mongo.db.mars_facts
    NASA_scraped_info = scrape_mars.scrape()
    mars_facts.update({}, NASA_scraped_info, upsert=True)
    return "Scraping Mars"



if __name__ == "__main__":
    app.run(debug=True)
