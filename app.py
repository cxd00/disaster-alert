from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)
subscribers = {}
subscribers["s"] = []
subscribers["s"].append({
    "number" : 9197445964,
    "zip" : 27599
})
subscribers["s"].append({
    "number" : 3363920218,
    "zip" : 27599
})
subscribers["s"].append({
    "number" : 9196567826,
    "zip" : 27599
})

class Subscriber(Resource):
    def get(self, number):

        for s in subscribers["s"]:
            if s["number"] == int(number):
                return s, 200
        return "Subscriber not found", 404

    def post(self): # adds new

        parser = reqparse.RequestParser()
        parser.add_argument("zip")
        parser.add_argument("number")
        args = parser.parse_args()

        for s in subscribers["s"]:
            if s["number"] == int(args["number"]):
                return "{} has already registered".format(args["number"]), 400
        
        subscriber = {
            "number": int(args["number"]),
            "zip": int(args["zip"])
        }

        subscribers["s"].append(subscriber)
        with open("data.json", "w") as outfile:
            json.dump(subscribers, outfile)
        return subscriber, 201

    def put(self, number): # updates
        parser = reqparse.RequestParser()
        parser.add_argument("zip")
        args = parser.parse_args()

        for s in subscribers["s"]:
            if s["number"] == int(number):
                s["zip"] = args["zip"]
                return s, 200
        
        subscriber = {
            "number": number,
            "zip": args["zip"]
        }

        subscribers["s"].append(subscriber)
        return subscriber, 201

    def delete(self, number):
        global subscribers
        subscribers["s"] = [s for s in subscribers if not s["number"] == int(number)]
        return "{} is deleted.".format(number), 200

@app.route('/')
def show():
    return render_template('index.html')

@app.route('/data', methods=["GET"])
def getJson():
    data = open("data.json").read()
    return jsonify(data)

api.add_resource(Subscriber, "/subscriber/")
app.run(debug=True)