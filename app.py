import os 
from flask import Flask, redirect, render_template, url_for, request
# from dotenv import load_env

# load_env()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.template.html')


















if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP'),
        port = os.environ.get('PORT'),
        debug = True
    )


