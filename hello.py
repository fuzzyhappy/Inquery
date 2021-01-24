import re

from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
# Use a service account
cred = credentials.Certificate('boilermake-8-project-firebase-adminsdk-n45vg-c326d22181.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

query_ref = db.collection(u'profdata')

app = Flask(__name__)
returnData = {}

def process(s):
  # converts to lowercase
  s = s.lower()
  # removes punctuation
  s = re.sub(r'[^\w\s]', '', s)
  # converts words to root words (stemming)
  porter = PorterStemmer()
  s = " ".join([porter.stem(word) for word in nltk.tokenize.word_tokenize(s)])
  return s
    
@app.route('/', methods = ['GET'])
def default():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html', data = returnData);

@app.route('/', methods = ['POST'])
def retrieve():    
    returnData.clear()
    docs = db.collection(u'profdata').stream()
    for doc in docs:
        if (u'researchArea' in doc.to_dict() and process(request.form[u'area']) in doc.to_dict()[u'researchArea']):
            returnData[doc.id] = doc.to_dict()
    return redirect('/results')

if __name__ == '__main__':
    app.run(debug=True)
