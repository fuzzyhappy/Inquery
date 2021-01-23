from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import spacy

# Use a service account
cred = credentials.Certificate('boilermake-8-project-firebase-adminsdk-n45vg-c326d22181.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

query_ref = db.collection(u'profdata')

app = Flask(__name__)
def check_sim(query, words):
    nlp = spacy.load('en_vectors_web_lg')
    max_sim = 0
    doc1 = nlp(query)
    for word in words:
        doc2 = nlp(word)
        sim = doc1.similarity(doc2)
        if sim > max_sim:
            max_sim = sim
    return max_sim
    
@app.route('/', methods = ['GET'])
def default():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def retrieve():
    returnData = {}
    docs = db.collection(u'profdata').stream()
    for doc in docs:
        if (u'researchArea' in doc.to_dict() and check_sim(request.form[u'area'], doc.to_dict()[u'researchArea']) >=.70):
            print(f'{doc.id} => {doc.to_dict()}')
            returnData[doc.id] = doc.to_dict()
    return render_template('index.html', data = returnData)

if __name__ == '__main__':
    app.run(debug=True)
