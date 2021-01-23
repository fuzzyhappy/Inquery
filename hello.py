from flask import Flask, render_template, request, redirect

app = Flask(__name__)

testData = { "bob" : {"contact" : "bob@lmao.com", "department" : "cs departmnet", "area" : "memes", "links" : "somelink.com"},
"yeet" : {"contact" : "xd@lmao.com", "department" : "cs departmnet", "area" : "minecraft", "links" : "morelinks.com"},
"name1" : {"contact" : "kjl@kjl.com", "department" : "cs departmnet", "area" : "data", "links" : "morelinksssss.com"},
"babooshka" : {"contact" : "pp@pp.com", "department" : "cs departmnet", "area" : "memes", "links" : "virus.com"},
"nam2" : {"contact" : "dffds@dsf.com", "department" : "cs departmnet", "area" : "minecraft", "links" : "cancer.gov"}
}
    

@app.route('/', methods = ['GET'])
def default():
    return render_template('index.html')


@app.route('/', methods = ['POST'])
def retrieve():
    returnData = {}
    for name in testData:
        if testData[name]["area"] == request.form['area']:
            returnData[name] = testData[name]
    return render_template('index.html', data = returnData)

    

@app.route('/add', methods = ['POST'])
def add_name():
    name = request.form['name']
    NAMES.append({'name' : name})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)