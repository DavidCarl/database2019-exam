from flask import Flask, url_for, jsonify,render_template

from flask_restful import Resource, Api, request
import mysql, mongodb

app = Flask(__name__)
api = Api(app)

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


class q1(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data['db_type'] == 'mysql':
            return jsonify(mysql.q1(json_data['city']))
        else:
            return jsonify(mongodb.q1(json_data['city']))

class q2(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data['db_type'] == 'mysql':
            return jsonify(mysql.q2(json_data['title']))
        else:
            return jsonify(mongodb.q2(json_data['title']))

class q3(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data['db_type'] == 'mysql':
            return jsonify(mysql.q3(json_data['author']))
        else:
            return jsonify(mongodb.q3(json_data['author']))

class q4(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data['db_type'] == 'mysql':
            return jsonify(mysql.q4(json_data['geolocation']))
        else:
            return jsonify(mongodb.q4(json_data['geolocation']))

api.add_resource(q1, '/api/1')
api.add_resource(q2, '/api/2')
api.add_resource(q3, '/api/3')
api.add_resource(q4, '/api/4')



if __name__ == "__main__":
    app.run(host='0.0.0.0')