import pickle
from data_model.helper_functions import clean_text
import os
from keras.models import load_model
from tensorflow.keras.preprocessing import sequence


def make_prediction(object):
    '''
    Accepts a json object that includes a 'name' key that is a string

    returns a binary prediction 
    '''
    
    # select the desired feature
    feature = object['name']

    # process the feature
    feature = clean_text(feature)
    
    # tokenize
    FILE_PATH = os.path.join(os.path.dirname(__file__), 'finished_models', 'new_tokenizer.pickle')
    token_maker = pickle.load(open(FILE_PATH, 'rb'))

    feature = [token_maker.texts_to_sequences(feature)]

    # pad sequence
    feature = sequence.pad_sequences(feature, maxlen=10, padding='post')
    
    # make prediction
    FILE_PATH = os.path.join(os.path.dirname(__file__), 'finished_models', 'basic_name_model.h5')
    model = load_model(FILE_PATH, compile=False)

    prediction = (model.predict(feature)[0][0] > 0.5).astype('int32')
    print(f'Confidence: {model.predict(feature)[0][0]}')
    return prediction
