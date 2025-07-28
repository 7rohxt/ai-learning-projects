from flask import Flask, render_template, request
from utils import preprocess
import pickle

app = Flask(__name__)

with open('text_classifier_pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        processed_input = preprocess(user_input) 
        prediction = pipeline.predict([processed_input])[0]  

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
