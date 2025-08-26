import streamlit as st
import os

from helper_functions_groq import groq_chat
from helper_functions_sql import reformat_json_response, execute_query, get_mysql_db_table_schema
from helper_functions_prompt import sql_prompt_generator, db_n_table_decider

st.set_page_config(page_title="SQL Chatbot with Groq", layout="wide")
st.title("SQL Quary Analyzer")

try:
    db_config = {
        "host": os.environ.get("DB_HOST"),
        "user": os.environ.get("DB_USERNAME"),
        "password": os.environ.get("DB_PSD"),
    }
    if not all(db_config.values()):
        st.error("Database credentials are not fully configured. Please check your .env file.")
        st.stop()
except Exception as e:
    st.error(f"Failed to load database configuration: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "sql_context_history" not in st.session_state:
    st.session_state.sql_context_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask a question about your airline..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                tables_decider_prompt = db_n_table_decider(user_query=user_query)
                llm1_response = groq_chat(messages=[{"role": "user", "content": tables_decider_prompt}])
                db_with_tables = reformat_json_response(llm1_response)

                sql_schema = get_mysql_db_table_schema(db_config=db_config, db_with_tables=db_with_tables)

                sql_prompt = sql_prompt_generator(user_query=user_query, sql_schema_for_tables=sql_schema)
                if st.session_state.sql_context_history:
                    formatted_history = "\n".join(st.session_state.sql_context_history)
                    sql_prompt = f"Chat History (for context):\n{formatted_history}\n\n---\n\n{sql_prompt}"
                
                sql_query_dict_str = groq_chat(messages=[{"role": "user", "content": sql_prompt}], model="llama3-70b-8192")
                sql_query_dict = reformat_json_response(sql_query_dict_str)
                sql_query = sql_query_dict.get('sql_query') if sql_query_dict else "SELECT 'Error: Could not generate query';"

                # --- THIS IS THE FIX ---
                # Extract the database name from the first LLM response
                database_name = list(db_with_tables.keys())[0] if db_with_tables else None
                if not database_name:
                    raise ValueError("Could not determine the database to query.")
                
                # Pass the database_name to the corrected execute_query function
                sql_result = execute_query(db_config,  sql_query)
                # --- END OF FIX ---

                response_prompt = (
                    "You are a helpful assistant. Provide a concise, natural language answer based on the user's query and the provided SQL result.\n\n"
                    f"User Query: {user_query}\n\n"
                    f"SQL Result: {str(sql_result)}"
                )
                final_response = groq_chat(messages=[{"role": "user", "content": response_prompt}])
                
                st.markdown(final_response)

                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
                st.session_state.sql_context_history.append(f"User: {user_query}")
                st.session_state.sql_context_history.append(f"Assistant SQL: {sql_query}")
                st.session_state.sql_context_history = st.session_state.sql_context_history[-10:]

            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
