from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('boilermake-8-project-firebase-adminsdk-n45vg-c326d22181.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

query_ref = db.collection(u'profdata')

app = Flask(__name__)

NAMES = []

@app.route('/hello')
def hello():
    return 'hello!';
@app.route('/')
def default():
    return render_template('index.html')
@app.route('/add', methods = ['POST'])
def add_name():
    name = request.form['name']
    NAMES.append({'name' : name})
    print(query_ref)
    return redirect('/')