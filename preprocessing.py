import numpy as np
import pandas as pd

def preprocessing(data):
    # Drop rows with missing values
    data = data.dropna()

    # Log transformation for the right-skewed columns
    data['total_rooms'] = np.log1p(data['total_rooms'])
    data['total_bedrooms'] = np.log1p(data['total_bedrooms'])
    data['population'] = np.log1p(data['population'])
    data['households'] = np.log1p(data['households'])

    # One-hot encoding on  'ocean_proximity' column 
    data = data.join(pd.get_dummies(data['ocean_proximity']).astype(int))

    data = data.drop('ocean_proximity', axis=1)

    # Create new features
    data['rooms_per_household'] = data['total_rooms'] / data['households']
    data['bedroom_ratio'] = data['total_rooms'] / data['total_bedrooms']
    data['population_per_household'] = data['population'] / data['households']

    return data