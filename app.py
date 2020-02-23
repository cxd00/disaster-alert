from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource, reqparse
import json
import http.client
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

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

@app.route('/messages', methods=["POST"])
def getStuff():
    req = request.json
    info = (req["from"], req["text"])
    if info[1] == "E":
        conn = http.client.HTTPSConnection("api.catapult.inetwork.com")
        payload = json.dumps({
            "from":"+19195335013",
            "to": "+1" + info[1],
            "text":"https://www.google.com/maps/dir/?api=1&origin=Your+Location&destination=Raleigh-Durham+International+Airport&travelmode=driving"
        })
        headers = {
            'Content-Type': 'application/json', 
            'Authorization': ' Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k='
        }
        conn.request("POST", "/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    elif info[1] == "S":
        nlpStuff(info)

    else:
        print("in F")
    return "why"


def nlpStuff(info):
    text = info[1]
    document = language.types.Document(
        content = text,
        language = "en",
        type='PLAIN_TEXT',
    )
    


api.add_resource(Subscriber, "/subscriber/")
app.run(debug=True, host="0.0.0.0")