import unittest

from app.pred_model import PredModel

MODEL_FILE = 'app/model/dummy.pickle'


class test_validation(unittest.TestCase):
    def setUp(self):
        self.model = PredModel(MODEL_FILE)

    def test_invalid(self):
        '''Invalid entry - should output False'''
        invalid_data = {'name': 'karen', 'has_cat': True}
        result = self.model.validate_input(invalid_data)
        self.assertFalse(result)

    def test_one_missing(self):
        ''' Lacking one variable -- should result be False '''

        '''EXPECTED_VARIABLES = ['name', 'desc', 'goal', 'keywords',
                      'disable_communication', 'country',
                      'currency', 'campaign_length']
        '''
        # Leave out 'disable_comunication'
        data = {'name': 'My Pet Project',
                'desc': 'I am doing something super cool so give me money!',
                'goal': '$5.00',
                'keywords': 'cool',
                'country': 'MyPrivateIdaho',
                'currency': 'bitcoin',
                'campaign_length': '25 years'}
        result = self.model.validate_input(data)
        self.assertFalse(result)

    def test_complete(self):
        ''' Complete variables -- should result True '''

        # Leave out 'disable_comunication'
        data = {'name': 'My Pet Project',
                'desc': 'I am doing something super cool so give me money!',
                'goal': '$5.00',
                'keywords': 'cool',
                'disable_communication': 'yes',
                'country': 'MyPrivateIdaho',
                'currency': 'bitcoin',
                'campaign_length': '25 years'}
        result = self.model.validate_input(data)
        self.assertTrue(result)


class test_predict(unittest.TestCase):
    def setUp(self):
        self.model = PredModel(MODEL_FILE)

    def test_output(self):
        ''' Should return single integer, 1 or 0 '''
        data = {'name': 'My Pet Project',
                'desc': 'I am doing something super cool so give me money!',
                'goal': '$5.00',
                'keywords': 'cool',
                'disable_communication': 'yes',
                'country': 'MyPrivateIdaho',
                'currency': 'bitcoin',
                'campaign_length': '25 years'}
        result = self.model.predict(data)
        self.assertIn(result, [1, 0])


if __name__ == '__main__':
    unittest.main()
