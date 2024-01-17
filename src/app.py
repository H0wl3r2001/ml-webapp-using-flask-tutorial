#import os
#os.environ['FLASK_ENV'] = 'production'

import flask
from flask import Flask, render_template, request, redirect, url_for
from pickle import load
import regex as re

vector = load(open("models/tfidf.sav", "rb"))
model = load(open("models/SVM.sav", "rb"))

app = Flask(__name__)

def preprocess_text(text):
    # Remove any character that is not a letter (a-z) or white space ( )
    text = re.sub(r'[^a-z ]', " ", text)
    
    # Remove white spaces
    text = re.sub(r'\s+[a-zA-Z]\s+', " ", text)
    text = re.sub(r'\^[a-zA-Z]\s+', " ", text)

    # Multiple white spaces into one
    text = re.sub(r'\s+', " ", text.lower())

    # Remove tags
    text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", text)

    return text.split()


def predict_sentiment(str_):
    sentence = [preprocess_text(str_)]
    sentence_vector = vector.transform(sentence).toarray()
    prediction = model.predict(sentence_vector)
    if prediction == 1:
        return 'SPAM'
    else:
        return 'Not a spam email'

@app.route('/', methods=['GET', 'POST'])
def spampage():
    answer = ''
    result = ''

    if request.method == 'POST' and 'review' in request.form:
        answer = request.form.get('review')
        if answer is None:
            result = 'Enter an sample email text'
        else:
            result = predict_sentiment(answer)

    return render_template('index.html', result=result)

app.run()