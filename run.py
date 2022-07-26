from flask import json,Blueprint
from flask import request
from flask import Flask
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.webhooksdb
GHactions = db.GHactions


@app.route('/receiver', methods=['POST'])
def api_gh_message():
    if request.method=='POST':
        info = json.dumps(request.json, indent=2)
        d = json.loads(info)
        id= d['pull_request']['base']['repo']['id']
        author = d['pull_request']['base']['user']['login']
        action = d['action']
        to_branch = d['pull_request']['head']['label']
        from_branch = d['pull_request']['base']['label']
        timestamp = d['pull_request']['head']['repo']['created_at']

        GHactions.insert_one({'id': id, 'author': author,'to_branch':to_branch, 'from_branch':from_branch, 'timestamp':timestamp, 'action':action})
        return redirect('index.html')
    
    return render_template('index.html')

@app.route('/')
def index():
    all_data =list( GHactions.find())
    
    return render_template('index.html', data = all_data)  

if __name__ == '__main__': 
    app.run(debug=True)
