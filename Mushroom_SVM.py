import numpy as np
from sklearn import model_selection as ms, svm
import pandas as pd
from pymongo import MongoClient
import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
import base64

uri = "mongodb://mushroom-predictor:ZkoVuLdDDPS0gwI8zn4zMgjFRqMZyKKTwfYs94LOPcAnP69VB2kWjyE7OxXns4omwzbIreZPgtX8KmNrNde4JQ==@mushroom-predictor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mushroom-predictor@&retrywrites=false"
client = MongoClient(uri, ssl=True)
db = client.MushroomPredictor
mushroom_db = db.Mushroom

class Mushroom_SVM:
    def __init__(self):
        self.clf = None
        self.confidence = None

    def train(self):
        mushrooms = list(mushroom_db.find())
        df = pd.DataFrame(mushrooms)

        no_id = df.drop(['_id'], 1)
        X = np.array(no_id.drop(['class'], 1))
        y = np.array(df['class'])

        X_train, X_test, y_train, y_test = ms.train_test_split(X, y, test_size=0.2)

        self.clf = svm.SVC()

        self.clf.fit(X_train, y_train)
        self.confidence = self.clf.score(X_test, y_test)

    def predict(self, sample):
        return self.clf.predict(np.array([sample]))
    
    def get_graph(self, graph_type='basic'):
        mushrooms = list(mushroom_db.find())
        df = pd.DataFrame(mushrooms)

        if (graph_type == 'basic'):
            # Basic graph calculations and assignements
            categories = ['Poisonous', 'Edible']
            poisonous_freq = len(df[df['class'] == 1]) / len(df) * 100
            edible_freq = len(df[df['class'] == 2]) / len(df) * 100
            frequencies = [poisonous_freq, edible_freq]

            # Creation of the graph
            fig = plt.figure(figsize=(4,5))

            plt.pie(frequencies, autopct='%0.2f%%')
            plt.axis('equal')
            plt.legend(categories)
            plt.title('Edible VS Poisonous')

            # Saving the graph to a stream of bytes
            fig_data = BytesIO()
            fig.savefig(fig_data, format='png')

            return base64.b64encode(fig_data.getvalue()).decode('utf-8').replace('\n', '')
