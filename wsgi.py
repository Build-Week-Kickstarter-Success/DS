# Installed libraries
from flask import Flask, jsonify

# Local libraries
from pred_model import PredModel


APP = Flask(__name__)

# todo: name for the pickled model
MODEL_FILE = None


@APP.route('/')
def root():
    return 'Welcome to the rest of your life.'


@APP.route('/campaign', methods=['GET', 'POST'])
def campaign():
    # todo: get campaign info from web folks, predict,
    # return results as json. Not even sure yet which
    # method(s), etc.

    # todo: get request object. PredModel will handle
    # preprocessing (e.g., encoding variables, whatever
    # the model needs as input)
    input = None

    model = PredModel(MODEL_FILE)
    prediction = model.predict(input)

    # todo: If we need to do any other massaging before packing
    # and shipping as JSON

    return jsonify(prediction)
