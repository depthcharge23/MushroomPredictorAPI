from flask import Flask, jsonify, request
from Mushroom_SVM import Mushroom_SVM

svm = Mushroom_SVM()
svm.train()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello World!'

@app.route('/predict-mushroom', methods=['POST'])
def predict_mushroom():
    data = request.get_json()

    prediction = svm.predict(data['data'])

    return jsonify({
        'confidence': svm.confidence,
        'prediction': int(prediction[0])
    })

if __name__ == '__main__':
    app.run()
    