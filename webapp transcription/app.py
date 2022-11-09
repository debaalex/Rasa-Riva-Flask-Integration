from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import json
import par_jump
import par_jump_stream

app = Flask(__name__, template_folder='Templates')
context_set = ""


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        name = request.form.get('name')  # retriving the .wav filename


        print(name)
        path = "/Users/alexdebertolis/Desktop/{}".format(name)  # building the path arg
        valRec = par_jump.runTranscript(path)
        print (valRec)

        return render_template("index.html",val= valRec[0],timer= valRec[1],throughput= valRec[2],runtime=valRec[3],lat=valRec[4],audiolen=valRec[5] )


if __name__ == '__main__':
    app.run(debug=True)
