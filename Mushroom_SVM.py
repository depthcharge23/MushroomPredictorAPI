"""
    Mushroom_SVM.py is a class file that was created to hold the Mushroom_SVM class. We need this class so we can generate
    a Mushroom_SVM object in the app.py file. It is import to store this as an object so we only need to train the SVM once
    and then we can continually make predictions against that trained model.

    This class was created mainly to perform the SVM train and predict operations, but it hold other functionalities such as:
        - Connecting to Azure Cosmos DB (MongoDB flavor) to fetch the mushroom data that will be used to train the SVM
        - Generate pie, bar, and heat map graphs
        - Tag the values of a property as either poisonous or edible

    Author:
        Aaron M. Mathews

    Date:
        5/19/2020
"""

import numpy as np
from sklearn import model_selection as ms, svm
import pandas as pd
from pymongo import MongoClient
import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from Mushroom_Map import Mushroom_Map
import seaborn as sns

mushroom_db = None

# Connect to the Azure Cosmos DB to retrieve the mushroom data
try:
    uri = "mongodb://mushroom-predictor:ZkoVuLdDDPS0gwI8zn4zMgjFRqMZyKKTwfYs94LOPcAnP69VB2kWjyE7OxXns4omwzbIreZPgtX8KmNrNde4JQ==@mushroom-predictor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mushroom-predictor@&retrywrites=false"
    client = MongoClient(uri, ssl=True)
    db = client.MushroomPredictor
    mushroom_db = db.Mushroom

    print('\nSuccessful MongoDB connection to the Mushroom collection...')
except:
    print('\nAn error occurred when connecting to the Mushroom MongoDB collection...')
    raise Exception('MongoDB error')

class Mushroom_SVM:

    # A basic constructor that defines the clf (classifer) property which will hold the SVM classifier, and
    # the confidence property that will store the confidence level of the classifier
    def __init__(self):
        self.clf = None
        self.confidence = None

    # This function will train the SVM classifier using the data stored in the Azure Cosmos DB
    def train(self):

        # Fetch all data from the Azure Cosmos DB and turn it into a DataFrame object
        mushrooms = list(mushroom_db.find())
        df = pd.DataFrame(mushrooms)

        # Drop the "_id" column that is added by the Azure Cosmos DB this field will mess up the SVM
        no_id = df.drop(['_id'], 1)

        # Create X which will be a DataFrame object of all of the other properties aside from the class property
        X = np.array(no_id.drop(['class'], 1))

        # Createy which will be a DataFrame object of only the class property
        y = np.array(df['class'])

        # Split the data into train and testing groups with a 80/20 split respectively
        X_train, X_test, y_train, y_test = ms.train_test_split(X, y, test_size=0.2)

        # Initialize the SVM object
        self.clf = svm.SVC()

        # Train and score the classifier
        self.clf.fit(X_train, y_train)
        self.confidence = self.clf.score(X_test, y_test)

    # This method runs the prediction using the classifier generated in the train() method
    def predict(self, sample):
        return self.clf.predict(np.array([sample]))

    # This method creates the graphs using the mushroom data from the Azure Cosmos DB
    def get_graph(self, graph_type='pie', prop='class'):

        # Get the data from the Azure Cosmos DB
        try:
            mushrooms = list(mushroom_db.find())
        except:
            print('\nAn internal occurred when calling the MongoDB Mushroom collection...')
            raise Exception('MongoDB error')

        # Create a DataFrame object of the mushroom data
        df = pd.DataFrame(mushrooms)

        # Initialzie a map object. This object holds all of the property values and their
        # corresponding values that are user friendly
        mm = Mushroom_Map().data

        # Create figure object
        fig = plt.figure(figsize=(5, 4))
        fig_data = BytesIO()

        # Create a pie graph
        if (graph_type == 'pie'):

            # Null check the prop value
            if prop != '':

                # Get a map of the prop values
                prop_map = mm[prop]

                # Sort the unique values that exist in the data frame column
                column_vals = sorted(df[prop].unique())

                # Create an array to store the percentage frequency of each value
                # showing up in the column
                freqs = []

                # Get a list of labels for a given prop
                x_labels = prop_map[0]

                # Loop through the unique column vals and get their percentage frequency of occurance
                for val in column_vals:
                    freqs.append(len(df[df[prop] == val]) / len(df) * 100)

                # Create the pie graph using the matplotlib
                plt.pie(freqs, autopct='%0.2f%%')
                plt.axis('equal')
                plt.legend(x_labels)
                plt.title(prop.capitalize())

                fig.savefig(fig_data, format='png')

        # Create a bar graph
        elif (graph_type == 'bar'):

            # Null check the prop value
            if prop != '':

                # Get a map of the prop values
                prop_map = mm[prop]

                # Sort the unique values for a given dataframe column
                x_vals = sorted(df[prop].unique())
                y_vals = []

                # Get a list of the user friendly prop values
                x_labels = prop_map[0]

                # Loop through the unique dataframe vals and get a count for each one
                for val in x_vals:
                    y_vals.append(len(df[df[prop] == val]))

                # Create the bar graph using matplotlib
                plt.bar(range(len(x_vals)), y_vals)

                ax = plt.subplot()
                ax.set_xticks(range(len(x_vals)))
                ax.set_xticklabels(x_labels, rotation=50)

                plt.title(prop.capitalize())

                fig.savefig(fig_data, format='png')

        else:
            print('\nThe following graph type is not a valid option: ' + graph_type)
            raise Exception('Invalid graphy type error')
        
        # Return the base64 encoded string to be sent through the HTTP protocol
        return base64.b64encode(fig_data.getvalue()).decode('utf-8').replace('\n', '')

    # Create a map for a given property that shows whether each unique value for that prop
    # shows up on either poisonous mushrooms, edible mushrooms, or both
    def map_data(self, prop):

        # Get the mushroom data from the Azure Cosmos DB
        try:
            mushrooms = list(mushroom_db.find())
        except:
            print('\nAn internal occurred when calling the MongoDB Mushroom collection...')
            raise Exception('MongoDB error')

        # Create a DataFrame object of the mushroom data
        df = pd.DataFrame(mushrooms)

        # Initialzie a map object. This object holds all of the property values and their
        # corresponding values that are user friendly
        mm = Mushroom_Map().data

        # Get the user friendly class values
        class_map = mm['class']

        # Get the user friendly values for a given prop
        prop_map = mm[prop]

        # Create dataframe of the given prop and class values
        data = df[[prop, 'class']]

        p_or_e = {}

        # Loop through each row in data and check to see if that prop_val is in the map
        # If the prop is not in the map, and it and the class_val to the map.
        # If the prop is in the map, check to see if it has the class_val if it has the class_val do nothing.
        # If the prop is in the map, check to see if it has the class_val if it doesn't have the class_val add the class_val.
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

        # Return the map
        return p_or_e

    # Generate a heat map for a given prop
    def heat_map_data(self, prop):

        # Get the mushroom data from the Azure Cosmos DB
        try:
            mushrooms = list(mushroom_db.find())
        except:
            print('\nAn internal occurred when calling the MongoDB Mushroom collection...')
            raise Exception('MongoDB error')

        # Create a DataFrame object of the mushroom data
        df = pd.DataFrame(mushrooms)

        # Initialzie a map object. This object holds all of the property values and their
        # corresponding values that are user friendly
        mm = Mushroom_Map().data

        # Get the user friendly class values
        class_map = mm['class']

        # Get the user friendly values for a given prop
        prop_map = mm[prop]

        heat_map = {}

        # Loop through the class_map keys (Poisonous and Edible)
        for i in range(1, len(class_map.keys())):
            p_and_e_pert = {}

            # Loop through the prop_map keys (any possible value for the property)
            for j in range(1, len(prop_map.keys())):

                # Generate a percentage for that prop and add it to the property in the map
                p_and_e_pert[prop_map[j]] = len(df[(df[prop] == j) & (df['class'] == i)]) / len(df[df[prop] == j]) * 100

            # Add the object to the class property
            heat_map[class_map[i]] = p_and_e_pert       

        # Turn the map into a DataFrame object
        heat_df = pd.DataFrame(heat_map)    
        
        # Create a heat map using the seaborn library
        fig = plt.figure(figsize=(7,4))
        fig_data = BytesIO()

        sns.heatmap(heat_df, linewidths=.5)
        plt.yticks(rotation=0)

        fig.savefig(fig_data, format='png')

        # Return the base64 encoded string to be sent through the HTTP protocol
        return base64.b64encode(fig_data.getvalue()).decode('utf-8').replace('\n', '')
        