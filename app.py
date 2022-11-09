from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import json
import par_jump

app = Flask(__name__, template_folder='Templates')
context_set = ""


@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'GET':
        # fetching the user input and sending to rasa
        val = str(request.args.get('text'))  # from the html form
        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data,
                            headers=headers)  # retriving RASA output
        res = res.json()
        val2 = res[0]['text']
        return render_template('index.html', val=val2)

    if request.method == 'POST':
        name = request.form.get('name')  # retriving the .wav filename
        path = "/Users/alexdebertolis/Downloads/{}".format(name)  # building the path arg
        valRec = par_jump.runTranscript(path)

        data = json.dumps({"sender": "Rasa", "message": valRec[0]})  # fetching the user transcribed input and sending
        # to rasa
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
        res = res.json()
        val2 = res[0]['text']
        print(res)
        return render_template('index.html',val=val2,trans=valRec[0], timer=valRec[1])

if __name__ == '__main__':
    app.run(debug=True)
