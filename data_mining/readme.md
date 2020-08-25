**Data Mining**

A basic ETL pipeline to take from the kickstarter scraper website:
![][https://webrobots.io/kickstarter-datasets/]

*etl.py*

The app to reset and update the database containing kickstarter data.

Use:

python etl.py reset

Will reset the database, loading data from the raw_data.csv file in the model/data directory.

python etl.py update <file>

Will add data drawn from the scraper site can be one or more of the files in the url sub-
directory. E.g.,

python etl.py update 2018

will add the zip files listed in the 2018.txt file. Multiple files can be used, e.g.

python etl.py update 2018 2019