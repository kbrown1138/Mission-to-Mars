# Import dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
mars = db.mars

# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
@app.route("/")
def home():
    mars_data = db.mars.find_one()
    return render_template("index.html", mars_data = mars_data)

# Create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
@app.route("/scrape")
def web_scrape():
    mars_data = db.mars
    mars_info = scrape_mars.scrape()
    mars_data.update({}, mars_info, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)