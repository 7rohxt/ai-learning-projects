import numpy as np
import pandas as pd
import pickle

def load_data():
    return pd.read_csv("housing.csv")


def load_model():
    with open("./models/cali_forest.pickle", 'rb') as f:
        model = pickle.load(f)


def preprocessing(data):
    # Log transformation for the right-skewed columns
    data['total_rooms'] = np.log1p(data['total_rooms'])
    data['total_bedrooms'] = np.log1p(data['total_bedrooms'])
    data['population'] = np.log1p(data['population'])
    data['households'] = np.log1p(data['households'])

    # One-hot encoding on  'ocean_proximity' column 
    data = data.join(pd.get_dummies(data['ocean_proximity']).astype(int))

    data = data.drop('ocean_proximity', axis=1)

    # Create new features
    data['rooms_per_household'] = np.log1p(data['total_rooms'] / data['households'])
    data['bedroom_ratio'] = np.log1p(data['total_bedrooms'] / data['total_rooms'])

    return data


def get_unique_ocean_proximity(data):
    return data["ocean_proximity"].unique().tolist()
