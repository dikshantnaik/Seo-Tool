from xml.dom.expatbuilder import theDOMImplementation
from flask import Flask, render_template
import views
import sheets
from threading import Thread
import requests
app = Flask(__name__)
thread = None


@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/execute")
def execute():
    # return views.Main()
    global thread
    print("--------------------------------")
    print("        SCRIPT STARTING ")
    print("--------------------------------")

    thread =Thread(name="main",target=views.Main)
    if thread.is_alive() == False:
        thread.start()
        return """
        <h1>Execution Started ...<br>
        Please don't Relode or Close this Page <br> 
        It'll take a 3-4 minute to update the Google Sheets if no error Occurs <br><br>
        <span font-color="red"> Redirection you to Spreadsheet in some Seconds
        <h1>

        """
    else:
        return "Script Ruinning"


@app.route("/getAhref")
def getAhref():
    print("--------------------------------")
    print("        SCRIPT STARTING[AHREF]  ")
    print("--------------------------------")
    thread = Thread(name="ahref",target=views.get_ahref_ur_dr)
    if thread.is_alive()==False:
        thread.start()
        return """
            <h1>Execution Started ...<br>
            Please don't Relode or Close this Page <br> 
            It'll take a 3-4 minute to update the Google Sheets if no error Occurs <br><br>
            <span font-color="red"> Redirection you to Spreadsheet in some Seconds
            <h1>

            """

        
    else:
        return "Script Ruinning"

   
@app.route("/checkStatus")
def checkIsAlive():
    try:
        if thread.isAlive()==True:
            return "<h1> The Script is Running "
            # print()
        elif views.error != "":
            return "<h1> Some Erorr Occured <h1> <br> <h2>"+views.error+"<h2>"
        elif thread==None:
            return "<h1> The Script isn't Running "
        else:
            return "Script isn't Running"
    except AttributeError:
        return "<h1> Script Isn't Running"
    
