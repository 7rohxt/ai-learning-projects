
# Fake Reviews Classifier

A web-based application that uses a machine learning model to detect whether a product review is **genuine** or **computer-generated**.

<!-- ![screenshot](static/demo_screenshot.png) -->

---

## Features

- Pretrained machine learning pipeline: `CountVectorizer` + `TF-IDF` + classifier  
- Web interface built with Flask  
- Custom text preprocessing:
  - Lowercasing
  - HTML tag removal
  - Tokenization
  - Stopword removal
  - **Lemmatization** (chosen over stemming for better semantic preservation)
- Classifies reviews into:
  - **Genuine review**
  - **Computer-generated review**
- Clean and minimal HTML/CSS UI  
- Easily deployable on AWS EC2 using Gunicorn and Nginx

---

## Demo

Try entering a sample review like:

- `"This product is amazing! Truly satisfied."`
- `"My car smells no different after 3 weeks. Snake oil."`

The app will classify whether the review is likely **human-written** or **AI-generated**.

---

## Tech Stack

- **Backend**: Flask, Python  
- **ML Libraries**: scikit-learn, nltk  
- **Frontend**: HTML, CSS  
- **Deployment**: Gunicorn, Nginx, AWS EC2

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/7rohxt/llm-retail-assistant.git
cd llm-retail-assistant
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Project Structure

.
├── text-classifier-app
│   ├── app.py                   # Flask app
│   ├── utils.py                 # Preprocessing logic
│   ├── templates/
│   │   └── index.html           # Frontend HTML
│   ├── static/
│   │   └── style.css            # Frontend CSS
│   └── text_classifier_pipeline.pkl  # Trained ML pipeline
├── requirements.txt             # Python dependencies
├── fake_reviews.ipynb           # Model development notebook
├── fake_reviews_dataset.csv     # Dataset used for training
├── .gitignore
└── README.md


---

## Model Pipeline

### Preprocessing Steps

- Lowercasing  
- HTML tag removal  
- Tokenization  
- Stopword removal  
- Lemmatization  

### Vectorization

- `CountVectorizer` → `TF-IDF`


---

## Deployment Guide (AWS EC2)

For production deployment, use Gunicorn as the WSGI server and Nginx as the reverse proxy.

The Deployment Guide includes step-by-step instructions to:

- Set up an EC2 instance  
- Configure the virtual environment  
- Run Gunicorn as a systemd service  
- Configure Nginx to proxy requests to the application

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it.