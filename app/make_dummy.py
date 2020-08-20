'''
Make a pickled DummyModel
'''
import pickle

from app.dummy import DummyModel


dm = DummyModel()
pickle.dump(dm, open('app/dummy.pickle', 'wb'))
