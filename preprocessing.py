import numpy as np
import pandas as pd

def preprocessing(data):
    # Drop rows with missing values
    data.dropna(inplace=True)

    # Log transformation for the right-skewed columns
    data['log_total_rooms'] = np.log1p(data['total_rooms'])
    data['log_total_bedrooms'] = np.log1p(data['total_bedrooms'])
    data['log_population'] = np.log1p(data['population'])
    data['log_households'] = np.log1p(data['households'])

    data.drop(['total_rooms', 'total_bedrooms', 'population', 'households'], axis=1, inplace=True)

    # One-hot encoding on  'ocean_proximity' column 
    data = data.join(pd.get_dummies(data['ocean_proximity']).astype(int))

    data.drop('ocean_proximity', axis=1, inplace=True)

    # Create new features
    data['rooms_per_household'] = data['log_totalrooms'] / data['log_households']
    data['bedroom_ratio'] = data['log_total_bedrooms'] / data['log_total_rooms']
    data['population_per_household'] = data['log_population'] / data['log_households']

    # z-score transformation
    for j in data.columns:
        mean = data[j].mean()
        std_dev = data[j].std()
        data[j] = (data[j] - mean) / std_dev 

    return data