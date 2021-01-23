from flask import Flask, render_template, request, redirect

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
    return redirect('/')