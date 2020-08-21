# Installed libraries
from flask import Flask, jsonify, render_template, request

# Local libraries
from app.pred_model import PredModel


APP = Flask(__name__)

# todo: name for the pickled model
MODEL_FILE = 'app/model/dummy.pickle'


@APP.route('/')
def root():
    return render_template('root.html')


@APP.route('/campaign', methods=['GET', 'POST'])
def campaign():
    # todo: get campaign info from web folks, predict,
    # return results as json. Not even sure yet which
    # method(s), etc.

    # todo: get request object. PredModel will handle
    # preprocessing (e.g., encoding variables, whatever
    # the model needs as input)

    # Determine request method and fetch parameters
    if request.method == 'POST':
        input = dict(request.form)
    elif request.method == 'GET':
        input = dict(request.args)

    model = PredModel(MODEL_FILE)
    prediction = model.predict(input)

    # todo: If we need to do any other massaging before packing
    # and shipping as JSON
    input['prediction'] = prediction

    return jsonify(input)
