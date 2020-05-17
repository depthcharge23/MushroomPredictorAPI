from flask import Flask, jsonify, request, send_file
from Mushroom_SVM import Mushroom_SVM
from pymongo import MongoClient

users_db = None
svm = None

try:
    uri = "mongodb://mushroom-predictor:ZkoVuLdDDPS0gwI8zn4zMgjFRqMZyKKTwfYs94LOPcAnP69VB2kWjyE7OxXns4omwzbIreZPgtX8KmNrNde4JQ==@mushroom-predictor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mushroom-predictor@&retrywrites=false"
    client = MongoClient(uri, ssl=True)
    db = client.Users
    users_db = db.Users

    print('\nSuccessful MongoDB connection to the User collection...')
except:
    print('\nAn error occurred when connecting to the MongoDB User collection...')

try:
    svm = Mushroom_SVM()
    svm.train()

    print('\nSuccessfully trained the machine learning model...')
except:
    print('\nAn error occurred when triaing the machine learning model...')

app = Flask(__name__)

@app.route('/predict-mushroom', methods=['POST'])
def predict_mushroom():
    data = None

    try:
        data = request.get_json()['data']
    except:
        print('\nAn error occurred when getting the data value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'
        })

    try:
        prediction = svm.predict(data)

        print('Successful mushroom prediction for data: ' + data)
        return jsonify({
            'confidence': svm.confidence,
            'prediction': int(prediction[0])
        })
    except:
        print('\nAn error occurred when running the SVM prediction...')
        print('Data that caused error: \n' + data)
        
        return jsonify({
            'error': 'An internal error occurred...'
        })
    
@app.route('/get-graph', methods=['POST'])
def get_graph():
    graph_type = None
    prop = None

    try:
        graph_type = request.get_json()['graphType']
    except:
        print('\nAn error occurred when getting the graphType value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'
        })

    try:
        prop = request.get_json()['prop']
    except:
        print('\nAn error occurred when getting the prop value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })
    
    try:
        image = svm.get_graph(graph_type, prop)

        print('\nSuccessful graph generation for:')
        print('Graph Type: ' + graph_type + '\n' + 'Property: ' + prop)
        return jsonify({
            'image': image
        })
    except:
        print('\nAn error occured when generating a graph for:')
        print('Graph Type: ' + graph_type + '\n' + 'Property: ' + prop)

        return jsonify({
            'error': 'An internal error occurred...'    
        })

@app.route('/get-user', methods=['POST'])
def get_user():
    username = None
    password = None

    try:
        username = request.get_json()['username']
    except:
        print('\nAn error occurred when getting the username value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    try:
        password = request.get_json()['password']
    except:
        print('\nAn error occurred when getting the password value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    try:
        users = list(users_db.find({
            'username': username,
            'password': password
        }))
        
        if len(users) > 0:
            print('\nSuccessful user login for user: ' + username)

            return jsonify({
                'status': 'valid'
            })
        else:
            print('\nUnsuccessful user login for user: ' + username)

            return jsonify({
                'status': 'invalid'
            })

    except:
        print('\nAn internal occurred when calling the MongoDB User collection...')

        return jsonify({
            'error': 'An internal error occurred...'
        })

@app.route('/map-data', methods=['POST'])
def map_data():
    prop = None

    try:
        prop = request.get_json()['prop']
    except:
        print('\nAn error occurred when getting the prop value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    try:
        data = svm.map_data(prop)

        print('\nSuccessful data mapping for prop: ' + prop)
        return jsonify(data)
    except:
        print('\nAn error occurred when mapping the property: ' + prop)

        return jsonify({
            'error': 'An internal error occurred...'    
        })

@app.route('/heat-map-data', methods=['POST'])
def heat_map_data():
    prop = None

    try:
        prop = request.get_json()['prop']
    except:
        print('\nAn error occurred when getting the prop value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    try:
        image = svm.heat_map_data(prop)

        print('\nSuccessful heat-map for prop: ' + prop)
        return jsonify({
            'image': image
        })
    except:
        print('\nAn error occurred when creating the heat map for prop value: ' + prop)

        return jsonify({
            'error': 'An internal error occurred...'    
        })
