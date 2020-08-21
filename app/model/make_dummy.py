'''
Make a pickled DummyModel
'''
import pickle

from app.model.dummy import DummyModel


dm = DummyModel()
pickle.dump(dm, open('app/model/dummy.pickle', 'wb'))
