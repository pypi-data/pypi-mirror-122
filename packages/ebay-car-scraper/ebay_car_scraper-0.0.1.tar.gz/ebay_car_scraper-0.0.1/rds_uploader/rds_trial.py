import sys

import pandas as pd
import psycopg2
from psycopg2 import errors
from sqlalchemy import create_engine
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'aicoredb.cjpo05djrpn0.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = 'Orebach94*'
PORT = 5432
DATABASE = 'postgres'

#conn = psycopg2.connect("dbname=dbname user=user")
conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, port=PORT, host=HOST)
cur = conn.cursor()
#pg = '''DROP table IF EXISTS cars '''
#pg = "DROP table IF EXISTS cars"
pg = "DROP TABLE IF EXISTS cars"
print(pg)
cur.execute(pg)
conn.commit()
cur.execute("CREATE TABLE cars (manufacturer VARCHAR(255), model VARCHAR(255), sale_price VARCHAR(255), year VARCHAR(255), transmission VARCHAR(255), fuel VARCHAR(255), mileage VARCHAR(255), condition VARCHAR(255), location VARCHAR(255), contact_number VARCHAR(255))")
conn.commit()
# except psycopg2.errors.DuplicateTable:
#     print('exists')
#
# else:
#     try:
#      cur.execute(" TABLE cars (manufacturer VARCHAR(255), model VARCHAR(255), sale_price VARCHAR(255), year VARCHAR(255), transmission VARCHAR(255), fuel VARCHAR(255), mileage VARCHAR(255), condition VARCHAR(255), location VARCHAR(255), contact_number VARCHAR(255))")
#     except:
#         pass
# if
# except psycopg2.errors.InFailedSqlTransaction:
#
#     print('Exists')
#
# else:
#     pass


#cars_data_df.to_sql('cars', engine, if_exists='replace', index=False)

#conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
with open(r"C:\Users\Simeon\PycharmProjects\pythonProject2\AiCore Substitute lecture videos & revision py_files\car_scraper package project 2\car_scraper\car_data_df.csv", 'r') as f:
    cars_data_df = pd.read_csv(f, index_col=0)
    engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    engine.connect()
    cars_data_df.to_sql('cars', engine, if_exists='replace', index=False)

cur.execute("SELECT * FROM cars")
result = cur.fetchall()
for r in result:
    print(r)

conn.close()
with open(r"C:\Users\Simeon\PycharmProjects\ebay_car_scraper_pypi\README.md", r) as a:
    long_description = a.read()

#     cars_data_df.to_sql('cars', engine, if_exists='replace', index=False)

#     next(f) # Skip the header row.
#     cur.copy_from(f, 'cars', sep=',')
#     conn.commit()

# with cur.cursor() as cur:
#     # Print all the tables from the database
# cur.execute("SELECT * FROM cars")
# result = cur.fetchall()
# for r in result:
#     print(r)