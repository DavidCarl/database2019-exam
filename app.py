from flask import Flask, url_for, jsonify,render_template
app = Flask(__name__)

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
    return render_template("search_location.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')