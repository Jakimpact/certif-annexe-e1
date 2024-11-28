import os
import csv

import pandas as pd
import pyodbc


# Variables
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path).rsplit("/", 1)[0]
extract_path = dir_path + "/extracts/bdd_tables"
errors_path = extract_path + "/errors"
sql_server = os.getenv("sql_server")
bdd_name = os.getenv("bdd_name")
username = os.getenv("username")
password = os.getenv("password")
schema_names = ("Production", "Sales", "Person")

# Connexion à la BDD Azure
conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={sql_server};DATABASE={bdd_name};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")
cursor = conn.cursor()

# Récupération des noms de table 
placeholders = ', '.join(['?'] * len(schema_names))
query = f"""
    SELECT TABLE_SCHEMA + '.' + TABLE_NAME AS FULL_TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA IN ({placeholders})
    AND TABLE_TYPE = 'BASE TABLE';
"""
params = schema_names
cursor.execute(query, params)
table_infos = cursor.fetchall()
table_names = [table[0] for table in table_infos]

# Récupération des tables
table_errors = []

for table in table_names:
        try:
            query = f"""SELECT * FROM {table}"""
            cursor.execute(query)
            result = cursor.fetchall()
            col_names = [column[0] for column in cursor.description]

            with open(f"{extract_path}/{table}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow(col_names)
                for row in result:
                    writer.writerow(row)

        except pyodbc.Error as e:
            table_errors.append([table, e])

# Listes des tables non récupérées et des erreurs
os.makedirs(errors_path, exist_ok=True)
with open(f"{errors_path}/errors.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(["Table", "Erreur"])
    for error in table_errors:
        writer.writerow(error)