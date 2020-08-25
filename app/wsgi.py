# Installed libraries
from flask import Flask, jsonify, render_template, request

# Local libraries
from app.pred_model import PredModel


APP = Flask(__name__)

# todo: name for the pickled model
MODEL_FILE = 'app/model/dummy.pickle'


@APP.route('/')
def root():
    '''Return readme page'''
    return render_template('root.html')


@APP.route('/campaign', methods=['GET', 'POST'])
def campaign():
    '''
    Accept input for the predictive model, and return prediction or
    error.

    Accepts either POST or GET methods.

    Returns output and HTML response code (200 for success, 400 for
    bad request if incomplete input)
    '''

    # Determine request method and fetch parameters
    if request.method == 'POST':
        input = dict(request.form)
    elif request.method == 'GET':
        input = dict(request.args)

    model = PredModel(MODEL_FILE)
    if not model.validate_input(input):
        output = 'Key Error: incorrect input variables'
        result = 400
    else:
        output = model.predict(input)
        result = 200

    # todo: If we need to do any other massaging before packing
    # and shipping as JSON

    return jsonify(output=output), result


if __name__ == '__main__":
    APP.run()
