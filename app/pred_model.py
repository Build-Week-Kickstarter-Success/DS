# Import libraries
import pickle
import numpy as np
# todo

# from data_model.model_prediction import make_prediction
from data_model.model_prediction import make_prediction


'''
Expected inputs:
name: name of the project

desc: description of project

goal: the goal (amount) required for the project

keywords: keywords which describe project

disable communication: whether the project authors has disabled
communication option with people donating to the project

country: country of project author

currency: currency in which goal (amount) is required
campaign length: the length of the campaign
'''

EXPECTED_VARIABLES = ['name', 'desc', 'goal', 'keywords',
                      'disable_communication', 'country',
                      'currency', 'campaign_length']


class PredModel():
    '''
    Load, instantiate, and wrap predictive model
    '''
    def __init__(self):
        # todo: import pickled model from unit4, and load
        try:
            self.model = make_prediction
        except Exception as err:
            raise err

    def validate_input(self, campaign):
        '''
        Validates input for the model.

        Arguments:
            campaign - the variables received in the HTML request

        Return:
            Boolean, True if valid input, otherwise False
        '''
        # Expected variables, one of each. Make local copy.
        variables = EXPECTED_VARIABLES.copy()

        # count each present variable, and remove from expected list
        # to avoid duplicates
        expected_count = len(variables)
        count = 0
        for key in campaign.keys():
            if key in variables:
                # This is also where we may want to validate types?
                # todo
                variables.remove(key)
                count += 1
        if count != expected_count:
            return False

        if campaign['disable_communication'].lower() not in ('yes', 'no',
                                                             'true', 'false',
                                                             '1', '0'):
            return False
        return True

    def predict(self, campaign):
        '''
        Accept input, send to predictive model, and accepts result.
        Perform any preprocessing of input for model (including put input
        into correct shape as (1, n) size array, where n is number of
        input features)

        Arguments:
            campaign - validated inputs from HTML request

        Return:
            Binary result of model, 0 or 1.
        '''
        try:
            # Convert variables to expected values
            if campaign['disable_communication'].lower() in ('yes', 'true'):
                campaign['disable_communication'] = True
            else:
                campaign['disable_communication'] = False
            campaign['goal'] = float(campaign['goal'])
            campaign['campaign_length'] = int(campaign['campaign_length'])

            # get prediction
            result = self.model(campaign)
        except Exception as err:
            raise err

        # Do any processing before returning.

        return result
