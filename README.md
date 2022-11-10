# Rasa-Riva-Flask-Integration
 
This repository contain an example of integration between the riva asr services and a chatbot built with RASA open source.
This work aims to be a modular architecture that can be useb by whoever as a basis to build a chatbot using RASA and Riva, here you can find:
- a directory that contains the script of a simple chatbot (covid-19 datas in italy)
- a directory that contains files of a only transcription web app
- a directory that contains files for a chatbot web app (only textual)
- a web app tha integrates all of the above

The depht and the complexity of every single component can be override as desired.

Requirements and release info:

- In order to use Riva ASR is needed a machine with Nvidia GPu (here we've provide an automated ssh connection that was our case solution)
- This scripts use Riva 1.10 but the version can be easily upgraded
- Riva wheel is installed in a docker so you need to install Docker to be able to run Riva CLI commands


