import numpy as np
import pandas as pd
import pickle

def load_data():
    return pd.read_csv("housing.csv")


def load_model():
    global model

    with open("./models/cali_forest.pickle", 'rb') as f:
        model = pickle.load(f)
    return model


def preprocessing(data):
    data['total_rooms'] = np.log1p(data['total_rooms'])
    data['total_bedrooms'] = np.log1p(data['total_bedrooms'])
    data['population'] = np.log1p(data['population'])
    data['households'] = np.log1p(data['households'])

    data = data.join(pd.get_dummies(data['ocean_proximity']).astype(int))
    data = data.drop('ocean_proximity', axis=1)

    data['rooms_per_household'] = np.log1p(data['total_rooms'] / data['households'])
    data['bedroom_ratio'] = np.log1p(data['total_bedrooms'] / data['total_rooms'])

    return data


def preprocess_user_input(data):
    if data['ocean_proximity'].iloc[0] == "ISLAND":
        data['ocean_proximity'] = "NEAR OCEAN"

    data['total_rooms'] = np.log1p(data['total_rooms'])
    data['total_bedrooms'] = np.log1p(data['total_bedrooms'])
    data['population'] = np.log1p(data['population'])
    data['households'] = np.log1p(data['households'])
 
    data = data.join(pd.get_dummies(data['ocean_proximity']).astype(int))

    expected_cols = ['<1H OCEAN', 'INLAND',
                     'NEAR BAY', 'NEAR OCEAN']

    for col in expected_cols:
        if col not in data.columns:
            data[col] = 0
    
    data = data.drop('ocean_proximity', axis=1)

    data['rooms_per_household'] = np.log1p(data['total_rooms'] / data['households'])
    data['bedroom_ratio'] = np.log1p(data['total_bedrooms'] / data['total_rooms'])

    return data   


def get_unique_ocean_proximity(data):
    return data["ocean_proximity"].unique().tolist()


def predict_home_price(housing_median_age, total_rooms, total_bedrooms,
            population, households, median_income,
            ocean_proximity='INLAND',
            longitude=36.5, latitude=-119.5,
            model=None):

    input_data = pd.DataFrame([{
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity
    }])

    processed_data = preprocess_user_input(input_data)

    prediction = np.round(model.predict(processed_data))

    return prediction[0]   


if __name__ == '__main__':
    load_data()
    load_model()
    print(predict_home_price(41, 880,129,322,126,8.3,'NEAR BAY', -122.23, 37.88, model))