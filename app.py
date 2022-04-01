from flask import Flask, render_template
import views
import sheets
from threading import Thread
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/execute")
def execute():
    # return views.Main()
    thread =Thread(name="main",target=views.Main)
    if thread.is_alive() == 0:
        thread.start()
    return """
    <meta http-equiv = "refresh" content = "5; url = https://docs.google.com/spreadsheets/d/1zJAhm3UoSxiF4ne1degW6uUuP2pLxw9rYckmF4jho0M/edit#gid=0" />
    <h1>Execution Started ...<br>
    Please don't Relode or Close this Page <br> 
    It'll take a 3-4 minute to update the Google Sheets if no error Occurs <br><br>
    <span font-color="red"> Redirection you to Spreadsheet in some Seconds
    <h1>

    """
