from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

class AgeImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.age_median = X["Age"].median()
        return self

    def transform(self, X):
        X = X.copy()
        X["Age"] = X["Age"].fillna(self.age_median)
        return X

class FeatureEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.encoder.fit(X[["Sex", "Embarked"]])
        return self

    def transform(self, X):
        X = X.copy()
        encoded_array = self.encoder.transform(X[["Sex", "Embarked"]])
        encoded_df = pd.DataFrame(
            encoded_array, 
            columns=self.encoder.get_feature_names_out(["Sex", "Embarked"]),
            index=X.index
        )
        return pd.concat([X, encoded_df], axis=1)

class FeatureDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop=None):
        self.columns_to_drop = columns_to_drop or ["Name", "Ticket", "Cabin", "Embarked", "Sex", "PassengerId", "Embarked_nan"]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop(columns=self.columns_to_drop, errors="ignore")