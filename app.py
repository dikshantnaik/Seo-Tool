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
    main_obj = views.Main
    main_obj.Main()
    # thread =Thread(name="main",target=main.Main)
    # if thread.is_alive() == 0:
    #     thread.start()
    return "heh"
@app.route("/execute2")
def execute2():
    URL = "http://da-checker-tool2.herokuapp.com/execute"
    requests.get(URL)
    # <meta http-equiv = "refresh" content = "5; url = https://docs.google.com/spreadsheets/d/1zJAhm3UoSxiF4ne1degW6uUuP2pLxw9rYckmF4jho0M/edit#gid=0" />
    return """
    <h1>Execution Started ...<br>
    Please don't Relode or Close this Page <br> 
    It'll take a 3-4 minute to update the Google Sheets if no error Occurs <br><br>
    <span font-color="red"> Redirection you to Spreadsheet in some Seconds
    <h1>

    """
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
    
