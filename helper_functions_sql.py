import mysql.connector
import json

def get_mysql_table_schema(db_config, tables):
    """
    Connects to a MySQL database and returns the CREATE TABLE statements for the specified tables.

    Parameters:
        host (str): Hostname or IP of the MySQL server.
        user (str): MySQL username.
        password (str): MySQL password.
        database (str): Name of the database.
        tables (list): List of table names to fetch CREATE TABLE statements for.

    Returns:
        dict: Dictionary with table names as keys and their CREATE TABLE SQL statements as values.
    """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    schema = {}
    for table in tables:
        try:
            # print(f"Fetching schema for: {table}")
            cursor.execute(f"SHOW CREATE TABLE `{table}`;")
            result = cursor.fetchone()
            if result:
                schema[table] = result[1]
        except mysql.connector.Error as err:
            print(f"Error fetching CREATE TABLE for {table}: {err}")
    cursor.close()
    conn.close()
    return schema


def get_mysql_db_table_schema(db_config, db_with_tables):
    """
    Connects to a MySQL server and returns CREATE TABLE statements as plain text
    for specified tables across multiple databases.

    Parameters:
        db_config (dict): MySQL connection config (host, user, password).
        db_with_tables (dict): { database_name: [table1, table2, ...] }

    Returns:
        str: SQL script with CREATE TABLE statements for all tables.
    """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    schema_text = ""

    for db_name, tables in db_with_tables.items():
        try:
            cursor.execute(f"USE `{db_name}`;")
            schema_text += f"\n-- Database: {db_name}\n"
        except mysql.connector.Error as err:
            schema_text += f"\n-- Error using database {db_name}: {err}\n"
            continue

        for table in tables:
            try:
                cursor.execute(f"SHOW CREATE TABLE `{table}`;")
                result = cursor.fetchone()
                if result:
                    schema_text += f"\n-- Table: {table}\n{result[1]};\n"
            except mysql.connector.Error as err:
                schema_text += f"\n-- Error fetching CREATE TABLE for {table}: {err}\n"

    cursor.close()
    conn.close()
    return schema_text



def reformat_json_response(llm_response):
    """
    if the response has format like this
    ```json{ "flag": 1 }``` 
    then remove trailing character from it and send dictionary only
    """
    try:   
        
        if llm_response.startswith("```json"):
            cleaned_response = llm_response.strip("`").replace("json\n", "", 1).strip()
            print("cleNed response ", cleaned_response)
            llm_json = json.loads(cleaned_response)
        else:
            llm_json = json.loads(llm_response)
        return llm_json
    except Exception as e:
        print("Exception occurred while parsing JSON:", e)
    


def execute_query(db_config, query):
    """
    Executes a SQL query using mysql.connector and returns the result as a list of dictionaries.
    In case of errors, returns a dictionary with an "error" key.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}