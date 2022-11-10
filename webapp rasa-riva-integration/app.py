from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import json
import par_jump

app = Flask(__name__, template_folder='Templates')
context_set = ""


@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'GET': #metodo testuale
        val = str(request.args.get('text'))  # recupero del messaggio scritto nel form dall'utente
        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data,
                            headers=headers) # invio testo a rasa
        res = res.json()# recupero risposta chatbot
        val2 = res[0]['text']
        return render_template('index.html', val=val2) #render del template

    if request.method == 'POST': #medoto vocale
        name = request.form.get('name')  # recupero del nome del file .wav
        path = "/Users/alexdebertolis/Downloads/{}".format(name)  # costruzione del percorso del file
        valRec = par_jump.runTranscript(path) #esecuzione trascrizione

        data = json.dumps({"sender": "Rasa", "message": valRec[0]})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)# invio testo a rasa
        res = res.json()
        val2 = res[0]['text'] #recupero risposta chatbot
        print(res)
        return render_template("index.html",val= valRec[0],timer= valRec[1],throughput= valRec[2],
                               runtime=valRec[3],lat=valRec[4],audiolen=valRec[5] )
        #render del template con i dati raccolti

if __name__ == '__main__':
    app.run(debug=True)
