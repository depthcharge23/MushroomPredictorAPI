import numpy as np
from sklearn import model_selection as ms, svm
import pandas as pd
from pymongo import MongoClient
import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from Mushroom_Map import Mushroom_Map

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

    def get_graph(self, graph_type='pie', prop='class'):
        mushrooms = list(mushroom_db.find())
        df = pd.DataFrame(mushrooms)
        mm = Mushroom_Map().data

        fig = plt.figure(figsize=(5, 4))
        fig_data = BytesIO()

        if (graph_type == 'pie'):
            if prop != '':
                prop_map = mm[prop]
                column_vals = sorted(df[prop].unique())

                freqs = []
                x_labels = prop_map[0]

                for val in column_vals:
                    freqs.append(len(df[df[prop] == val]) / len(df) * 100)

                plt.pie(freqs, autopct='%0.2f%%')
                plt.axis('equal')
                plt.legend(x_labels)
                plt.title(prop.capitalize())

                fig.savefig(fig_data, format='png')

        elif (graph_type == 'bar'):
            if prop != '':
                prop_map = mm[prop]

                x_vals = sorted(df[prop].unique())
                y_vals = []

                x_labels = prop_map[0]

                for val in x_vals:
                    y_vals.append(len(df[df[prop] == val]))

                plt.bar(range(len(x_vals)), y_vals)

                ax = plt.subplot()
                ax.set_xticks(range(len(x_vals)))
                ax.set_xticklabels(x_labels, rotation=50)

                plt.title(prop.capitalize())

                fig.savefig(fig_data, format='png')
        
        return base64.b64encode(fig_data.getvalue()).decode('utf-8').replace('\n', '')

    def map_data(self, prop):
        mushrooms = list(mushroom_db.find())
        df = pd.DataFrame(mushrooms)
        mm = Mushroom_Map().data

        class_map = mm['class']
        prop_map = mm[prop]

        data = df[[prop, 'class']]

        p_or_e = {}
        for i in range(1, len(data)):
            row = data.iloc[i]
            prop_val = prop_map[row[0]]
            class_val = class_map[row[1]]

            try:
                x = p_or_e[prop_val]
                try:
                    x.index(class_val)
                except:
                    x.append(class_val)
            except:
                p_or_e[prop_val] = [class_val]

        return p_or_e

    def heat_map_data(self, prop):
        mushrooms = list(mushroom_db.find())
        df = pd.DataFrame(mushrooms)
        mm = Mushroom_Map().data

        class_map = mm['class']
        prop_map = mm[prop]

        heat_map = {}
        for i in range(1, len(prop_map.keys())):
            p_and_e_pert = {}
            for j in range(1, len(class_map.keys())):
                p_and_e_pert[class_map[j]] = len(df[(df[prop] == i) & (df['class'] == j)]) / len(df[df[prop] == i]) * 100

            heat_map[prop_map[i]] = p_and_e_pert            
                
        return heat_map
