# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection locally 
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# # Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_dict = mongo.db.mars_dict.find_one()
    # mars_dict = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    # mars_dict = mongo.db.collection
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.news()
    mars_data = scrape_mars.image()
    mars_data = scrape_mars.facts()
    mars_data = scrape_mars.hemispheres()
    mars_dict.update({}, mars_data, upsert=True)
    # mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)