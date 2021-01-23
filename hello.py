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
<<<<<<< HEAD
    
=======

testData = { "bob" : {"contact" : "bob@lmao.com", "department" : "cs departmnet", "area" : "memes", "links" : "somelink.com"},
"yeet" : {"contact" : "xd@lmao.com", "department" : "cs departmnet", "area" : "minecraft", "links" : "morelinks.com"},
"name1" : {"contact" : "kjl@kjl.com", "department" : "cs departmnet", "area" : "data", "links" : "morelinksssss.com"},
"babooshka" : {"contact" : "pp@pp.com", "department" : "cs departmnet", "area" : "memes", "links" : "virus.com"},
"nam2" : {"contact" : "dffds@dsf.com", "department" : "cs departmnet", "area" : "minecraft", "links" : "cancer.gov"}
}
def check_sim(word1, word2):
    nlp = spacy.load('en_vectors_web_lg')
    doc1 = nlp(word1)
    doc2 = nlp(word2)
    return doc1.similarity(doc2)
>>>>>>> ad3a98c55a87b0613cc99cdaa47231b75f592a20
@app.route('/', methods = ['GET'])
def default():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def retrieve():
    returnData = {}
    docs = db.collection(u'profdata').stream()
    for doc in docs:
        if (u'researchArea' in doc.to_dict() and request.form[u'area'], doc.to_dict()[u'researchArea']) >=.70):
            print(f'{doc.id} => {doc.to_dict()}')
            returnData[doc.id] = doc.to_dict()
    return render_template('index.html', data = returnData)

if __name__ == '__main__':
    app.run(debug=True)
