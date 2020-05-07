from flask import Flask, jsonify, request, send_file
from Mushroom_SVM import Mushroom_SVM

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
