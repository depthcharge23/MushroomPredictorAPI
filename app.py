"""
    app.py is the main file that is used for the Flask API in the Mushroom Predictor app. This file provides
    all of the HTTP routes to handle functions like making the mushroom prediction, signing in users, generating graphs,
    and tagging data.

    The Mushroom Predictor API is hosted on Microsoft Azure and uses an Azure Cosmos DB (MongoDB flavor) to store the mushroom data, and user data.

    The purpose of this file was for my capstone project for Western Governors University. The idea was a mobile app that could use an
    SVM to classify a mushroom based on a multitude of mushroom properties.

    Author: 
        Aaron M. Mathews

    Date:
        5/19/2020
"""

from flask import Flask, jsonify, request, send_file
from Mushroom_SVM import Mushroom_SVM
from pymongo import MongoClient

users_db = None
svm = None

# Connect to the Cosmos DB User collection
try:
    uri = "mongodb://mushroom-predictor:ZkoVuLdDDPS0gwI8zn4zMgjFRqMZyKKTwfYs94LOPcAnP69VB2kWjyE7OxXns4omwzbIreZPgtX8KmNrNde4JQ==@mushroom-predictor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mushroom-predictor@&retrywrites=false"
    client = MongoClient(uri, ssl=True)
    db = client.Users
    users_db = db.Users

    print('\nSuccessful MongoDB connection to the User collection...')
except:
    print('\nAn error occurred when connecting to the MongoDB User collection...')

# Train the svm model
try:
    svm = Mushroom_SVM()
    svm.train()

    print('\nSuccessfully trained the machine learning model...')
except:
    print('\nAn error occurred when triaing the machine learning model...')

# Create the Flask app
app = Flask(__name__)

# The POST route for predicting a mushroom
@app.route('/predict-mushroom', methods=['POST'])
def predict_mushroom():
    data = None

    # Get the data from the JSON body of the HTTP request
    try:
        data = request.get_json()['data']
    except:
        print('\nAn error occurred when getting the data value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'
        })

    # Attempt to use the data to make a prediction on what kind of mushroom
    # the user has.
    try:
        prediction = svm.predict(data)

        print('Successful mushroom prediction for data: ' + str(data))

        # Return the confidence of the prediction and the result of the prediction
        return jsonify({
            'confidence': svm.confidence,
            'prediction': int(prediction[0])
        })
    except:
        print('\nAn error occurred when running the SVM prediction...')
        print('Data that caused error: \n' + str(data))
        
        return jsonify({
            'error': 'An internal error occurred...'
        })
    
# The POST route for generating pie and bar graphs for a given prop
@app.route('/get-graph', methods=['POST'])
def get_graph():
    graph_type = None
    prop = None

    # Get the graphType from the JSON body of the HTTP request
    try:
        graph_type = request.get_json()['graphType']
    except:
        print('\nAn error occurred when getting the graphType value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'
        })

    # Get the prop from the JSON body of the HTTP request
    try:
        prop = request.get_json()['prop']
    except:
        print('\nAn error occurred when getting the prop value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })
    
    # Attempt to generate and image based on the graphType and prop
    try:
        image = svm.get_graph(graph_type, prop)

        print('\nSuccessful graph generation for:')
        print('Graph Type: ' + graph_type + '\n' + 'Property: ' + prop)

        # Return the image generated
        return jsonify({
            'image': image
        })
    except:
        print('\nAn error occured when generating a graph for:')
        print('Graph Type: ' + graph_type + '\n' + 'Property: ' + prop)

        return jsonify({
            'error': 'An internal error occurred...'    
        })

# The POST route to check to see if there is a valid user in the DB
@app.route('/get-user', methods=['POST'])
def get_user():
    username = None
    password = None

    # Get the username from the JSON body of the HTTP request
    try:
        username = request.get_json()['username']
    except:
        print('\nAn error occurred when getting the username value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    # Get the password from the JSON body of the HTTP request
    try:
        password = request.get_json()['password']
    except:
        print('\nAn error occurred when getting the password value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    # Atempt to find the user in the DB
    try:
        users = list(users_db.find({
            'username': username,
            'password': password
        }))
        
        # If users is greater than 0 there is a valid user so return "valid"
        if len(users) > 0:
            print('\nSuccessful user login for user: ' + username)

            return jsonify({
                'status': 'valid'
            })
        # If users is not greater than 0 there is not a valid user so return "invalid"
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

# The POST route to tag the data for a property as either "Piosounous" or "Edible"
@app.route('/map-data', methods=['POST'])
def map_data():
    prop = None

    # Get the prop from the JSON body of the HTTP request
    try:
        prop = request.get_json()['prop']
    except:
        print('\nAn error occurred when getting the prop value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    # Attempt to map the data prop
    try:
        data = svm.map_data(prop)

        print('\nSuccessful data mapping for prop: ' + prop)

        # Return the data map
        return jsonify(data)
    except:
        print('\nAn error occurred when mapping the property: ' + prop)

        return jsonify({
            'error': 'An internal error occurred...'    
        })

# The POST route that will generate a heat map graph for a given prop
@app.route('/heat-map-data', methods=['POST'])
def heat_map_data():
    prop = None

    # Get the prop from the JSON body of the HTTP request
    try:
        prop = request.get_json()['prop']
    except:
        print('\nAn error occurred when getting the prop value from the JSON body...')
        print('The body data that caused the error\n' + str(request.get_json()))

        return jsonify({
            'error': 'An internal error occurred...'    
        })

    # Attempt to generate the heat map image
    try:
        image = svm.heat_map_data(prop)

        print('\nSuccessful heat-map for prop: ' + prop)

        # Return the heat map image
        return jsonify({
            'image': image
        })
    except:
        print('\nAn error occurred when creating the heat map for prop value: ' + prop)

        return jsonify({
            'error': 'An internal error occurred...'    
        })
