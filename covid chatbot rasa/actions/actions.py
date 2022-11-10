import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAskCovidRegion(Action):

    def name(self) -> Text:
        return "action_info_covid_regioni"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get(
            "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json").json()
        entity_par=tracker.latest_message["entities"] #recupero delle entities contenute nell'ultimo messaggio
        check_slot = tracker.get_slot("regione") #recupero dello slot
        regione = ""
        parameter = ""
        print("last message x par:", entity_par, "\n")
        print(check_slot)

        if check_slot is not None:
            regione=check_slot
        message = "please enter a correct italian region name"

        for e in entity_par:
            if e['entity'] == "parameter":
                parameter = e['value']
                parameter= parameter.strip().title() #recupero parametro


        for data in response: #costruzione del messaggio output
            if data["denominazione_regione"] == regione.title():
                print(data)
                if parameter == "Actual Positive Cases":
                    message="Actual positive cases: " + str(data['nuovi_positivi'])
                elif parameter == "Hospitalized With Symptoms":
                    message = "Hospitalized with symptoms: " + str(data['ricoverati_con_sintomi'])
                elif parameter == "Intensive Care Unit":
                    message = "Intensive care unit: " + str(data['terapia_intensiva'])
                elif parameter == "Total Deceased":
                    message = "Total deceased: " + str(data['deceduti'])
                elif parameter == "General Situation":
                    message = "Actual positive cases: " + str(data['nuovi_positivi']) + " Hospitalized with symptoms: " + str(
                    data['ricoverati_con_sintomi']) + " Intensive care unit:" + str(
                    data['terapia_intensiva']) + " Total deceased:" + str(data['deceduti'])
                else: print("it wasnt possible to provide datas, sorry")

        print(message)
        dispatcher.utter_message( regione + ": \n" + message) #presentazione del messaggio

        return []


class ActionAskCovidItaly(Action):

    def name(self) -> Text:
        return "action_info_covid_ita"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global parameter
        response = requests.get(
            "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json").json()
        intent = tracker.latest_message["intent"]
        entity_par = tracker.latest_message["entities"]
        message1=""
        print("last message", intent)
        print("last message x par:", entity_par, "\n")

        for e in entity_par:
            if e['entity'] == "parameter":
                parameter = e['value']
                parameter= parameter.strip().title()

        for data in response:
            if data["stato"] == "ITA":
                print(data)
                if parameter == "Actual Positive Cases":
                    message1 = "Actual positive cases: " + str(data['nuovi_positivi'])
                elif parameter == "Hospitalized With Symptoms":
                    message1 = "Hospitalized with symptoms: " + str(data['ricoverati_con_sintomi'])
                elif parameter == "Intensive Care Unit":
                    message1 = "Intensive care unit: " + str(data['terapia_intensiva'])
                elif parameter == "Total Deceased":
                    message1 = "Total deceased: " + str(data['deceduti'])
                elif parameter == "General Situation":
                    message1 = "Actual positive cases: " + str(
                        data['nuovi_positivi']) + " Hospitalized with symptoms: " + str(
                        data['ricoverati_con_sintomi']) + " Intensive care unit:" + str(
                        data['terapia_intensiva']) + " Total deceased:" + str(data['deceduti'])
                else:
                    print("it wasnt possible to provide datas, sorry")

        print(message1)
        dispatcher.utter_message("Covid situation in Italy: "  + "\n" + message1)

        return []