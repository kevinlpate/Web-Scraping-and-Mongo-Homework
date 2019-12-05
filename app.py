from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_collection

@app.route("/")
def index():
    mars_collection_values = list(db.collection.find())
    print(mars_collection_values)
    mars_collection_values = mars_collection_values[0]
    return render_template("index.html",mars_collection_values = mars_collection_values)

@app.route('/scrape')
def scrape():
    data = scrape_mars.scrape()
    db.collection.delete_many({})
    db.collection.insert_one(data)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
