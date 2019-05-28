from flask import Flask, url_for, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
app = Flask(__name__)

GoogleMaps(app, key="AIzaSyBvmxwwqPXsP0_0LSSnv-vXVfm8Eu1iCUM")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search_city")
def search_city():
    return render_template("search_city.html")

@app.route("/search_title")
def search_title():
    return render_template("search_title.html")

@app.route("/search_author")
def search_author():
    return render_template("search_author.html")

@app.route("/search_location")
def search_location():
    mymap = Map(
        identifier="first-map",
        lat=55.770135, 
        lng=12.512226,
        markers=[(55.770135,12.512226)],
        maptype_control=False,
        streetview_control=False
    )
    return render_template("search_location.html", mymap=mymap)



if __name__ == "__main__":
    app.run(host='0.0.0.0')