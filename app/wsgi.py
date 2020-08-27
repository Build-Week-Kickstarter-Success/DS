# Installed libraries
from flask import Flask, jsonify, redirect, render_template, \
    request, url_for
from flask_bootstrap import Bootstrap

# Local libraries
from app.pred_model import PredModel
from app.forms import TestForm


APP = Flask(__name__)
Bootstrap(APP)

APP.config['SECRET_KEY'] = 'Its a secret to everyone'


@APP.route('/')
def root():
    '''Return readme page'''
    return render_template('root.html')


@APP.route('/test_api', methods=['GET', 'POST'])
def test_api():
    form = TestForm()
    if form.validate_on_submit():
        name = form.name.data
        desc = form.desc.data
        goal = form.goal.data
        keywords = form.keywords.data
        disable_communication = form.disable_com.data
        country = form.country.data
        currency = form.currency.data
        campaign_length = form.length.data
        return redirect(url_for('campaign',
                                name=name,
                                desc=desc,
                                goal=goal,
                                keywords=keywords,
                                disable_communication=disable_communication,
                                country=country,
                                currency=currency,
                                campaign_length=campaign_length))

    return render_template('test_api.html', form=form)


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

    try:
        model = PredModel()
        if not model.validate_input(input):
            output = 'Key Error: incorrect input variables'
            result = 400
        else:
            output = model.predict(input)
            result = 200
    except Exception:
        result = 500
        output = 'Internal error'
    finally:
        print(f'Result = {output}')
        return jsonify(output=output[0][0]), result


if __name__ == "__main__":
    APP.run()
