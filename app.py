from flask import Flask, render_template
import views
import sheets
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/execute")
def execute():
    urls = sheets.input_websites()
    views.get_da_pa_ss(urls)
    return "EXECUTED"