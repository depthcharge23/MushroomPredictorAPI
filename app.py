from flask import Flask, jsonify, request, send_file
from Mushroom_SVM import Mushroom_SVM
from pymongo import MongoClient

uri = "mongodb://mushroom-predictor:ZkoVuLdDDPS0gwI8zn4zMgjFRqMZyKKTwfYs94LOPcAnP69VB2kWjyE7OxXns4omwzbIreZPgtX8KmNrNde4JQ==@mushroom-predictor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mushroom-predictor@&retrywrites=false"
client = MongoClient(uri, ssl=True)
db = client.Users
users_db = db.Users

svm = Mushroom_SVM()
svm.train()

app = Flask(__name__)

@app.route('/predict-mushroom', methods=['POST'])
def predict_mushroom():
    data = request.get_json()

    prediction = svm.predict(data['data'])

    return jsonify({
        'confidence': svm.confidence,
        'prediction': int(prediction[0])
    })
    
@app.route('/get-graph', methods=['POST'])
def get_graph():
    graph_type = request.get_json()['graphType']
    prop = request.get_json()['prop']
    
    image = svm.get_graph(graph_type, prop)

    return jsonify({
        'image': image
    })

@app.route('/get-user', methods=['POST'])
def get_user():
    username = request.get_json()['username']
    password = request.get_json()['password']

    try:
        users = list(users_db.find({
            'username': username,
            'password': password
        }))
        
        if len(users) > 0:
            return jsonify({
                'status': 'valid'
            })
        else:
            return jsonify({
                'status': 'invalid'
            })

    except:
        return jsonify({
            'status': 'error'
        })

@app.route('/map-data', methods=['POST'])
def map_data():
    prop = request.get_json()['prop']

    return jsonify(svm.map_data(prop))
