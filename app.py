from flask import Flask, request, jsonify
from utils import load_data, load_model, get_unique_ocean_proximity
import pandas as pd

app = Flask(__name__)
data = load_data()
model = load_model()

@app.route('/get_ocean_proximity')
def get_ocean_proximity():
    return jsonify(get_unique_ocean_proximity(data))

if __name__ == "__main__":
    print("Starting")
    app.run()