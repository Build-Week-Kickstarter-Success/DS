# imports
import os
import pandas as pd
from sklearn.utils import resample
import category_encoders as ce
from sklearn.preprocessing import StandardScaler


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









