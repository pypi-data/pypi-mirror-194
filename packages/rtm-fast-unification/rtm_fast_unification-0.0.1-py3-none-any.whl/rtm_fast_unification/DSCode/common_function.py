import os

import pandas as pd
# import pyodbc
import requests
from scipy.sparse import issparse

api_url = "https://us-fast-dev-be.azurewebsites.net/api/native_query_response"



def check_path(relative_path):
    relative_path = "/"+relative_path if relative_path[0] not in ['\\', '/'] else relative_path
    parent_path = os.getcwd()
    if os.path.exists(parent_path+
            os.path.normpath(relative_path)) is True:
        return os.getcwd()+ os.path.normpath(relative_path)
    elif parent_path[len(parent_path)-len("\\app\\"):] == '\\app\\':
        return parent_path[:len(parent_path)-len("\\app\\")] + relative_path

def run_query(query, params):
    query = query.format(**params)
    todo = {
        "query":query,
        "params":[]
    }
    response = requests.post(api_url, json=todo)

    try:
        results = response.json()
    except Exception as e:
        print(e)
        results = e
    result1_df = pd.DataFrame(results['data'])
    return result1_df

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]

# for running code using local database for uk
# def run_query(query, params):
#     # connecting with UK database
#     server = "TIGER02076\MSSQL2019"
#     database = "MTUK2"
#     driver = "ODBC Driver 17 for SQL Server"
#     trusted_conn = "yes"

#     # creating connection string and establishing connection
#     cnxn = pyodbc.connect(
#         "DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_conn}".format(
#             driver=driver, server=server, database=database, trusted_conn=trusted_conn
#         )
#     )
#     # parameters are passed along with query
#     query = query.format(**params)

#     df = pd.read_sql_query(query, cnxn)
#     print(df.head())
#     return df
