from flask import Flask, request, jsonify, render_template
from utils import load_data, load_model, get_unique_ocean_proximity, predict_home_price

app = Flask(__name__)
data = load_data()
model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_ocean_proximity')
def get_ocean_proximity():
    return jsonify(get_unique_ocean_proximity(data))

@app.route('/predict_price', methods=['POST'])
def predict_price():
    user_input = request.get_json()
    try:
        prediction = predict_home_price(
            housing_median_age=user_input["housing_median_age"],
            total_rooms=user_input["total_rooms"],
            total_bedrooms=user_input["total_bedrooms"],
            population=user_input["population"],
            households=user_input["households"],
            median_income=user_input["median_income"],
            ocean_proximity=user_input.get("ocean_proximity", "INLAND"),
            longitude=user_input.get("longitude", 36.5),
            latitude=user_input.get("latitude", -119.5),
            model=model
        )
        return jsonify({"predicted_price": prediction})
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

