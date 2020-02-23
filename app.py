from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource, reqparse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import http.client
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud.language import types

cred = credentials.Certificate('./key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

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
    print(nlpStuff(("+19105995176", "I need water")))
    return render_template('index.html')

@app.route('/data', methods=["GET"])
def getJson():
    data = open("data.json").read()
    return jsonify(data)

@app.route('/messages', methods=["POST"])
def getStuff():
    global last
    req = request.json
    info = (req["from"], req["text"])
    if info[1] == "E":
        last = "E"
        conn = http.client.HTTPSConnection("api.catapult.inetwork.com")
        payload = json.dumps({
            "from":"+19195335013",
            "to": info[0],
            "text":"Evacuation route here: \nhttps://www.google.com/maps/dir/?api=1&origin=Your+Location&destination=Raleigh-Durham+International+Airport&travelmode=driving"
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
        last = "S" 
        conn = http.client.HTTPSConnection("api.catapult.inetwork.com")
        payload = json.dumps({
            "from":"+19195335013",
            "to": info[0],
            "text":"Enter what you either need or have for disaster relief!"
        })
        headers = {
            'Content-Type': 'application/json', 
            'Authorization': ' Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k='
        }
        conn.request("POST", "/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8")) 

    elif info[1] == "F":
        last = "F"
        conn = http.client.HTTPSConnection("api.catapult.inetwork.com")
        payload = json.dumps({
            "from":"+19195335013",
            "to": info[0],
            "text":"Enter the phone number of a person you want to check up on in one text message"
        })
        headers = {
            'Content-Type': 'application/json', 
            'Authorization': ' Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k='
        }
        conn.request("POST", "/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    elif last == "F":
        last == "A"
        conn = http.client.HTTPSConnection("api.catapult.inetwork.com")
        payload = json.dumps({
            "from":"+19195335013",
            "to": "+1"+info[1],
            "text":"{} wants to check up on you! Text them back to let them know you're okay".format(info[0])
        })
        headers = {
            'Content-Type': 'application/json', 
            'Authorization': ' Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k='
        }
        conn.request("POST", "/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    elif last == "S":
        last == "B"
        results = nlpStuff(info)
        for r in results:
            if r["part"] == "NOUN":
                item = r["word"]
        print(item)
        for r in results:
            txt_ref = db.collection(u'text-info')
            person = []
            if r["part"] == "VERB":
                if r["word"] in ["want", "need"]:
                    query_ref = txt_ref.where(u'word', u'==', item)
                    print(query_ref.toJSON())
                    for q in query_ref:
                        person.append(query_ref["user"])
                elif r["word"] in ["have"]:
                    query_ref = txt_ref.where(u'word', u'==', item)
                    for q in query_ref:
                        person.append(query_ref["user"])
        
        ppl = [str(ppl + j + "\n") for j in person]
        conn = http.client.HTTPSConnection("api.catapult.inetwork.com")
        payload = json.dumps({
            "from":"+19195335013",
            "to": info[0],
            "text":ppl
        })
        headers = {
            'Content-Type': 'application/json', 
            'Authorization': ' Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k='
        }
        conn.request("POST", "/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    return "why"


def nlpStuff(info):
    text = info[1]

    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_syntax(document, encoding_type=encoding_type)
    results = []
    for token in response.tokens:
        r = {
            u"user" : info[0],
            u"word" : str(token.text.content),
            u"part" : str(enums.PartOfSpeech.Tag(token.part_of_speech.tag).name)
        }
        print(r)
        results.append(r)
        doc_ref = db.collection(u'text-info').document()
        doc_ref.set(r)
    return results

    


api.add_resource(Subscriber, "/subscriber/")
app.run(debug=True, host="0.0.0.0")