import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    tokens = word_tokenize(text)

    cleaned = []
    for word in tokens:
        word = word.translate(str.maketrans('', '', string.punctuation))
        if word.isalpha() and word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            cleaned.append(lemma)

    return ' '.join(cleaned)