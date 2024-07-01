# Library imports
import pandas as pd
import numpy as np


import joblib

import matplotlib.pyplot as plt

import nltk
from flask import Flask, request, redirect, url_for, render_template
import os


app = Flask(__name__)
app.config['UPLOAD_FILE'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

tfidf= joblib.load('tfidf.pkl')

model = joblib.load('analyzer.pkl')


# creating a function for data cleaning
from custom_tokenizer_function import CustomTokenizer

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Define predict function
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    tweet= [str(x) for x in request.form.values()]
    prediction=model.predict((tfidf.transform(tweet))[0])
    if prediction==1:
        return render_template('index.html', prediction_text='non-depression')
    
    else:
        return render_template('index.html', prediction_text='depression')

@app.route('/upload_file', methods=['POST','GET'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FILE'], file.filename)
        file.save(filepath)
        return redirect(url_for('analyze_file', filename=file.filename))
    return redirect(request.url)

@app.route('/analyze/<filename>')
def analyze_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FILE'], filename)
    df = pd.read_csv(filepath)
    #if 'text' not in df.columns:
       # return "CSV file must have a 'text' column."
    
    tweet = df['text'].values
    

    predictions=model.predict((tfidf.transform(tweet)))
    df['sentiment'] = predictions

    non_depression = sum(df['sentiment'] )
    depression = len(predictions) - non_depression
   
    
    non_depression_percentage = "{:.2f}".format(( non_depression/ len(predictions)) * 100)
    depression_percentage = "{:.2f}".format((depression / len(predictions)) * 100)
    
    return render_template('index.html',non_depression_percentage=non_depression_percentage,depression_percentage=depression_percentage) 

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FILE']):
        os.makedirs(app.config['UPLOAD_FILE'])
    
    app.run(debug=True)




        












  
