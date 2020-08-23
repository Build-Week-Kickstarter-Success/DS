# imports
import os
import pandas as pd
from sklearn.utils import resample
import category_encoders as ce
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
import keras.backend as K


def load_data():
    FILE_PATH = os.path.join(os.getcwd(), 'data', 'initial_cleaned_data.csv')
    return pd.read_csv(FILE_PATH, index_col=None)

def upsample_minority(df):
    counts = df['final_status'].value_counts().index
    majority = counts[0]
    minority = counts[1]

    df_majority = df[df['final_status'] == majority]
    df_minority = df[df['final_status'] == minority]

    majority_class_size = len(df_majority)
    minority_class_size = len(df_minority)

    minority_upsampled = resample(df_minority, 
                replace=True, 
                n_samples=majority_class_size,
                random_state=42) 
    return pd.concat([df_majority, minority_upsampled])

def downsample_majority(df):
    counts = df['final_status'].value_counts().index
    majority = counts[0]
    minority = counts[1]

    df_majority = df[df['final_status'] == majority]
    df_minority = df[df['final_status'] == minority]

    majority_class_size = len(df_majority)
    minority_class_size = len(df_minority)

    majority_downsampled = resample(df_majority, 
                replace=False, 
                n_samples=minority_class_size,
                random_state=42) 
    return pd.concat([df_minority, majority_downsampled])

def my_split(df, year):
    train = df[df['launch_year'] < year]
    test = df[df['launch_year'] == year]
    return train, test

def model_prep(train, test, features, target, onehot=True, scale=True):
    encoder = ce.one_hot.OneHotEncoder(use_cat_names=True)
    scaler = StandardScaler()

    X_train = train[features]
    if onehot:
        X_train = encoder.fit_transform(X_train)
    if scale:
        X_train = scaler.fit_transform(X_train)

    y_train = train[target]

    X_test = test[features]
    if onehot:
        X_test = encoder.transform(X_test)
    if scale:
        X_test = scaler.transform(X_test)
    y_test = test[target]
    return X_train, y_train, X_test, y_test

def get_results(y_true, y_pred):
    accuracy_metric = accuracy_score(y_true, y_pred)
    roc_auc_metric = roc_auc_score(y_true, y_pred)
    f1_metric = f1_score(y_true, y_pred)

    print('-------------------------------')
    print(f'Accuracy Score: {accuracy_metric}')
    print(f'ROC AUC Score: {roc_auc_metric}')
    print(f'F1 Score: {f1_metric}')
    return

# code credit to https://medium.com/@aakashgoel12/how-to-add-user-defined-function-get-f1-score-in-keras-metrics-3013f979ce0d
def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val






