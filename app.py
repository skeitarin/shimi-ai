from flask import Flask, render_template, request

import multiprocessing as mp
import tensorflow as tf

import os, sys
import numpy as np
path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)
import modules.domain.index as d_index

app = Flask(__name__)

@app.route("/")
def poker():
    return render_template('poker.html')

@app.route("/poker/predict", methods=['POST'])
def poker_predict():
    data = request.get_json(force=True)
    result = d_index.predict(list(map(float, data)))
    return result

@app.route("/test")
def test():
    mes = "Hello World in templates"
    list = ["a1", "a2", "a3"]
    dict = {"name":"John", "age":24}
    bl = True
    return render_template('test.html', message=mes, list=list, dict=dict, bl=bl)

@app.route("/get")
def get():
    get_args = request.args.get("msg", "Not defined")
    return "Hello Wolrd " + get_args

@app.route("/post", methods=['POST'])
def post():
    post_args = request.form["msg"]
    return "Hello Wolrd " + post_args

if __name__ == "__main__":    
    app.debug = True
    app.run()