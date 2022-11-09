from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import json


app = Flask(__name__, template_folder='Templates')
context_set = ""


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        # fetching the user input and sending to rasa
        val = str(request.args.get('mess'))  # from the html form
        print(val)

        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data,
                            headers=headers)  # retriving RASA output
        res = res.json()
        val2 = res[0]['text']
        return render_template('index.html', val=val2)

    if __name__ == '__main__':
        app.run(debug=True)