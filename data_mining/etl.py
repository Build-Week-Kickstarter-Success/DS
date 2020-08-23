import os
import sys
import sqlite3
import glob
import zipfile
from urllib.request import urlretrieve

import pandas as pd


class KickstartDatabase():
    def __init__(self, db_connection, columns):
        self.connection = db_connection
        self.common_columns = columns

    def reset_db(self):
        '''
        Reset database with the initial contents from raw_data.csv
        '''
        # Retrieve CSV into dataframe and filter to just selected columns
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../model/data/raw_data.csv')
        df = pd.read_csv(filename)
        df = df[self.common_columns]

        # Create table in database, dropping if previously exists
        df.to_sql('kickstart', self.connection, if_exists='replace',
                  index=False)

    def update_db(self, zip_url):
        '''
        Retireve new datasets from https://webrobots.io/kickstarter-datasets/.
        In each dataset there is a zip file with individual CSV files. Open
        each and concatenate to the current data from the database, without
        introducing duplicates.

        We totally rewrite the DB table to also insure there are no duplicates
        from previous updates.

        Arguments:
            zip_url: the url to the zip file from
                https://webrobots.io/kickstarter-datasets/
        '''
        # Retrieve current data from database
        df = pd.read_sql('SELECT * FROM kickstart', self.connection)

        # Obtain the zip file with new data
        print('Fetching zip file...')
        csv_files = urlretrieve(zip_url)

        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, 'csv_files')

        # unzip into a local temp directory
        print('Extracting CSV files...')
        with zipfile.ZipFile(csv_files[0], 'r') as zip_ref:
            zip_ref.extractall(filepath)

        # process each CSV file
        filepath = os.path.join(dirname, 'csv_files/*.csv')
        count = 1
        for filename in glob.glob(filepath):
            print(f'Processing CSV file {count}\r', end='')

            # load and filter
            new_df = pd.read_csv(filename)

            # We'll drop any that are live or suspended, and get them
            # later when they have a final status
            cond = (new_df['state'] != 'live') & \
                (new_df['state'] != 'suspended')
            new_df = new_df[cond]

            # Convert to binary status
            new_df['state'] = new_df['state'].replace({'failed': 0,
                                                       'canceled': 0,
                                                       'successful': 1})

            # Convert columns and filter
            new_df = new_df.rename(columns={'blurb': 'desc',
                                            'state': 'final_status'})
            new_df = new_df[self.common_columns]

            # Remove used CSV file
            os.remove(filename)
            count += 1

            # concatenate to dataframe
            df = pd.concat([df, new_df], sort=False). \
                drop_duplicates(subset=['name'])

        # Update database, dropping an replacing table with larger dataframe
        print('\nWriting database...')
        df.to_sql('kickstart', self.connection, if_exists='replace',
                  index=False)


if __name__ == '__main__':
    common_columns = ['deadline',
                      'created_at',
                      'backers_count',
                      'launched_at',
                      'disable_communication',
                      'currency',
                      'name',
                      'country',
                      'goal',
                      'final_status',
                      'state_changed_at',
                      'desc']

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../model/data/kickstart.sqlite')
    connection = sqlite3.Connection(filename)
    ks_db = KickstartDatabase(connection, common_columns)

    if len(sys.argv) == 1:
        print('\'python etl.py reset\' to reset database')
        print('\'python etl.py update <file list>\' to add data')

    elif sys.argv[1] == 'reset':
        print('Resetting database to original dataset...')
        ks_db.reset_db()
    elif sys.argv[1]:
        years = sys.argv[2:]
        for year in years:
            print(f'Collecting {year}')

            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, f'urls/{year}.txt')

            with open(filename) as fp:
                Lines = fp.readlines()
                count = 1
                for line in Lines:
                    print(f'Processing file {count}')
                    ks_db.update_db(line)
                    count += 1
    else:
        print('Unrecognized parameter')
        print('\'python etl.py reset\' to reset database')
        print('\'python etl.py update <file list>\' to add data')

    print('Done!\n')
    connection.close()
