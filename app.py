from flask import Flask, jsonify, request, send_file
from Mushroom_SVM import Mushroom_SVM
import pyodbc

server = 'mushroom-predictor.database.windows.net'
database = 'mushroom-predictor'
username = 'ammathews'
password = '22ilbbid!4274'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';TRUSTED_CONNECTION=yes;')
cursor = cnxn.cursor()

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
        cursor.execute('SELECT COUNT(*) AS row FROM dbo.USERS u WHERE u.USER_NAME = ' + username + ' AND u.PASSWORD = ' + password)
        data = cursor.fetchone()
        print(data)
    except:
        print('error')

    return 'nice'
