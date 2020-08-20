'''
Dummy model: just returns 0 as prediction for testing purposes
'''


class DummyModel():
    def __init__(self):
        pass

    def fit(self, X, Y=None):
        return self

    def predict(self, X):
        return 0
