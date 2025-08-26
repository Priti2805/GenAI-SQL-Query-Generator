def sql_prompt_generator(user_query, sql_schema_for_tables):
    sql_prompt = (
                "You are an SQL query generator. Your job is to convert the user query into a valid MySQL query using the following schema or schema's:\n\n"
                f"{sql_schema_for_tables}\n\n"
                "Instructions:\n"
                "- Generate a MySQL query based on the given input query. Generate sql query with database name, for example SELECT * FROM database_name.table;\n"
                "- Ensure the query is syntactically correct.It should have ; at the end\n"
                "- Scehma from Tables from differnt databases are listed here, use it to generate complex query with join using different databases if required."
                "- Always output only a JSON object with a single key `sql_query`, whose value is the MySQL query string.\n"
                "- Ensure that string comparisons in the WHERE clause are case-insensitive using LOWER(column) = LOWER(value).\n"
                "- If the query contains aggregation (e.g., COUNT, SUM, AVG), include all non-aggregated columns in a GROUP BY clause.\n"
                "- Always add a LIMIT 10 if the query retrieves a list and doesn't already have a limit.\n"
                "- Do not include any explanation, formatting, or extra text.\n\n"
            )
    sql_prompt += f"Query: {user_query}"

    print(sql_prompt)
    return sql_prompt



def decide_tables(user_query):
    tables_decider = (
            f"""
            You are provided with a summary of several database tables and their contents. 
            Based on this information, analyze the given user query and determine which tables are most relevant for answering it.

            Table Summaries of passenger_system database:
            - passengers: Stores personal and contact details of passengers, with unique passenger_id, email, and phone
            - flight_passengers: Links passengers to flights with seat assignments, referencing both passengers and flights
            - connecting_flights: Tracks connecting flight details for passengers, linking main and connecting flights with optional notes.
            Task:
            Analyze the user query in the context of the table descriptions above. Based on the keywords, intent, and expected data involved, identify which tables are necessary to answer the query.
            Expected Output:
            Stirctly return a list of the relevant table names in the following format:
            ["passenger", "connecting_flights"]

            User query: {user_query}
        """)
    
    return tables_decider


def db_n_table_decider(user_query):
    db_table_dict = (f"""
        You are an intelligent assistant for airplane that identifies which database and table(s) are required to answer a user's query based on the following schema:

        Databases and Tables:
        - flights_system:
            - flights: Stores details of flight id, scheduled flights, including airplane, route, and flight number.
            - flight_status: Stores real-time status details of flight_ids from flights table, including timing, location, delays, and current status.             

        - passenger_system:
            - passengers: Stores personal and contact details of passengers, with unique passenger_id, email, and phone
            - flight_passengers: Links passengers to flights, from flights_system database using passenger flight id, with seat assignments, referencing both passengers and flights
            - connecting_flights: Tracks connecting flight details for passengers, linking main and connecting flights with optional notes.

        Task:
        Given a user query, identify and return:
        1. The most relevant database name(s).
        2. The most relevant table name(s).

        Output Format:
        Strictly return putput in below format
        {{
        "db1_name": ["table1", "table2"],
        "db2_name": ["table1"]
        }}

        Only include databases and tables that are directly needed to answer the query. Do not include explanations.
        User query: {user_query}             
        
        """)
    print("prompt is ...........................................\n ", db_table_dict)
    return db_table_dict