# DEPENDENCIES
from flask import Flask, render_template, redirect, Markup
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():
    # Find data
    mars_scrape = mongo.db.scrape.find()
    # return template and data
    return render_template("index.html", mars_scrape=mars_scrape)


# create route that runs scrape function
@app.route("/scrape")
def scrape():

    # Run scrape function
    scraped = scrape_mars.scrape_all()

    # Store results into a dictionary
    mars_data = {
        "content_title": scraped["content_title"],
        "content_paragraph": scraped["content_paragraph"],
        "featured_image_url": scraped["featured_image_url"],
        "mars_weather": scraped["mars_weather"],
        "html_table": scraped["html_table"],
        "hemisphere_image_urls": scraped["hemisphere_image_urls"]
    }

    # hemisphere_1 = {scraped["hemisphere_1"]}
    # hemisphere_2 = {scraped["hemisphere_2"]}
    # hemisphere_3 = {scraped["hemisphere_3"]}
    # hemisphere_4 = {scraped["hemisphere_4"]}

    # Delete collections and create again to reset data
    mongo.db.scrape.drop()
    mongo.db.create_collection("scrape")
    # mongo.db.hemisphere_1.drop()
    # mongo.db.create_collection("hemisphere_1")
    # mongo.db.hemisphere_2.drop()
    # mongo.db.create_collection("hemisphere_2")
    # mongo.db.hemisphere_3.drop()
    # mongo.db.create_collection("hemisphere_3")
    # mongo.db.hemisphere_4.drop()
    # mongo.db.create_collection("hemisphere_4")

    # Insert entry into database
    mongo.db.scrape.insert_one(mars_data)
    # mongo.db.hemisphere_1.insert_one(hemisphere_1)
    # mongo.db.hemisphere_2.insert_one(hemisphere_2)
    # mongo.db.hemisphere_3.insert_one(hemisphere_3)
    # mongo.db.hemisphere_4.insert_one(hemisphere_4)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
