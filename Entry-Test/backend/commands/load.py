import json
import os
import pandas as pd
import mysql.connector
from termcolor import colored

def load_dataset(file_path):
    l, file_extension = os.path.splitext(file_path)
    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif file_extension == '.json':
        return pd.read_json(file_path)
    elif file_extension == '.html':
        return pd.read_html(file_path)[0]
    elif file_extension == '.parquet':
        return pd.read_parquet(file_path)
    elif file_extension in ['.pkl', '.pickle']:
        return pd.read_pickle(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

# Connexion à MySQL
print("\n------------------------------------------")
print("| DATABASE CONNECTION")
print("------------------------------------------")

host = input('|> Provide your MySQL server host: ').strip() or "localhost"
port = input('|> Provide your MySQL server port: ').strip() or "3306"
user = input('|> Provide your MySQL username: ').strip() or "root"
password = input('|> Provide your MySQL password: ').strip() or "Maliba2002"
database_name = input('|> Provide the MySQL database name: ').strip() or "global_outlooks"

table_name = ""
try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database_name
    )
    cursor = conn.cursor()
    print(colored("✅ Successfully connected to MySQL!", 'green'))
except mysql.connector.Error as err:
    print(colored(f"❌ MySQL Connection Error: {err}", 'red'))
    exit(1)

# Boucle pour charger plusieurs datasets
while True:
    print("\n| LOAD INTO DATABASE")
    print("------------------------------------------")

    table_name = input('|> Provide the table name: ').strip() or "industry_trends"
    dataset_path = input('|> Provide the dataset directory path: ').strip()
    filename = input('|> Provide the dataset filename: ').strip()
    file_path = os.path.join(dataset_path, filename)

    try:
        df = load_dataset(file_path)
        data_records = df.to_dict(orient="records")
    except Exception as e:
        print(colored(f"❌ Error loading dataset: {e}", 'red'))
        continue
    
    columns = df.columns
    column_definitions = ", ".join([f"`{col}` TEXT" for col in columns])

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {column_definitions}
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print(colored(f"✅ Table `{table_name}` ready!", 'green'))

    insert_query = f"""
    INSERT INTO `{table_name}` ({", ".join([f"`{col}`" for col in columns])})
    VALUES ({", ".join(["%s"] * len(columns))})
    """
    data_values = [tuple(record.get(col, None) for col in columns) for record in data_records]

    try:
        cursor.executemany(insert_query, data_values)
        conn.commit()
        print(colored(f"✅ Inserted {cursor.rowcount} records into `{table_name}`!", 'green'))
    except mysql.connector.Error as err:
        print(colored(f"❌ Error inserting data: {err}", 'red'))
        conn.rollback()

    repeat = input("\nDo you want to insert another dataset? (yes/no): ").strip().lower()
    if repeat not in ['yes', 'y']:
        break

cursor.close()
conn.close()
print(colored("✅ MySQL connection closed.", 'yellow'))
