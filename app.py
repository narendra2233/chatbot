
import openai
import streamlit as st
import pandas as pd
import io
from dotenv import load_dotenv
import sqlite3
import os
from nemoguardrails import RailsConfig,LLMRails
load_dotenv()
# Function to get table columns from SQLite database
def get_table_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("Columns in the table:", columns)
    return [column[1] for column in columns]

# Function to generate SQL query from input text using ChatGPT
def generate_sql_query(table_name, text, columns):
    # OpenAI API key (replace this with your actual key or load from an environment variable)
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    prompt = f"""
You are a ChatGPT language model that can generate SQL queries.
Please provide a natural language input text, and I will generate the corresponding SQL query for you.
The table name is {table_name} and corresponding columns are {columns}.

Input: {text}
SQL Query:
"""
    config=RailsConfig.from_path("config2")
    app=LLMRails(config)
    print("Prompt for OpenAI API:", prompt)
    response = app.generate(
          # Use a valid model
        messages=[{"role": "user", "content": prompt}]
    )
    sql_query = response['content'].strip()
    #print("sql query from openai is :",sql_query)

    start = sql_query.find("```sql") + len("```sql")
    end = sql_query.find("```", start)
    
    # Extract and clean the SQL query
    if start != -1 and end != -1:
        result=sql_query[start:end].strip()
        return result
    else:
        return sql_query

    # Clean up the query string to remove markdown code block formatting
    

# Function to execute SQL query on SQLite database
def execute_sql_query(cursor, query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print("Query Result:", result)
        return result
    except sqlite3.OperationalError as e:
        result=" I'm here to assist you related to Tabular data"
        return result

# Function to get the response from GPT-3 or GPT-4
def get_bot_response(cursor, table_name, user_input, columns, excel_data=None):
    try:
        if excel_data is None:
            return "Error: No data uploaded. Please upload an Excel file first."
        
        if user_input:
                sql_query = generate_sql_query(table_name, user_input, columns)
                if sql_query:
                    result=execute_sql_query(cursor, sql_query)
                    if isinstance(result,str):
                        response=result
                    else:
                        response=st.dataframe(result)
                    

                    #result = st.dataframe(execute_sql_query(cursor, sql_query))
                    return response
                    
        else:
            return "Error: Please enter your input."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
def main():
    conn = sqlite3.connect("chatgb.db") 
    cursor = conn.cursor()

    # Streamlit app title
    st.title("AI Chatbot with Excel File Handling")

   # Function to display the greeting and instructions
    st.markdown("""
    <style>
       {
           margin: 0;
           padding: 0;
           box-sizing: border-box;
        }
       body {
         font-family: Arial, sans-serif;
         background-color: #f4f4f9;
         height: 100vh;
         display: flex;
         justify-content: center;
         align-items: center;
         padding: 20px;
}
.input-container {
  background-color: #ffffff;
  padding: 20px;
  width: 50%
}
       .container{

          display: flex;
          width: 100%;
          height: 100%;
          max-width: 1200px;

}
       .container .greeting-container {
          background-color: #00838f; 
            color: white; 
            padding: 30px; 
            border-radius: 10px;
            text-align: left;
            width: 100%;  /* Ensure it spans the width */
            margin: 0;    /* Remove any margin */
        }
.greeting-container h1 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.greeting-container p {
  font-size: 1.1rem;
  line-height: 1.6;
}

.instructions {
  text-align: left;
  margin-top: 20px;
}

.instructions h2 {
  font-size: 1.3rem;
  margin-bottom: 10px;
}

.instructions ol {
  list-style-type: decimal;
  padding-left: 20px;
}
        
    </style>
<div class="container">
    <div class="greeting-container">
        <h1>Hello and welcome! 👋</h1>
        <p>I'm your AI-powered assistant, here to help you solve queries related to your data.</p> 
        <h2>How to Get Started:</h2>
        <ol>
            <li>📂 <strong>Upload your Excel file</strong> below.</li>
            <li>Once uploaded, feel free to ask me anything about the data, such as:
                <ul>
                    <li>📊 <strong>Summary of the data</strong></li>
                    <li>🔢 <strong>Details about the columns</strong></li>
                    <li>📏 <strong>The shape of the dataset</strong></li>
                </ul>
            </li>
            <li>Let’s get started! Upload your file first, and then ask away!</li>
        </ol>
    </div>
    <div class="input-container"></div>
</div>
    """, unsafe_allow_html=True)


    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "excel_data" not in st.session_state:
        st.session_state.excel_data = None

    # Allow user to upload an Excel file
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        st.session_state.excel_data = pd.read_excel(uploaded_file)

    # Create a table in the SQLite database
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TRANSACTION1 (
        "Transaction ID" TEXT,
        "Transaction date" TEXT,
        "Client name" TEXT,
        "Transaction type" TEXT,
        "Transaction amount" REAL
    )""")

    if st.session_state.excel_data is not None and not st.session_state.excel_data.empty:
        st.session_state.excel_data.to_sql('TRANSACTION1', conn, if_exists='replace', index=False)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input after file is uploaded
    if uploaded_file is not None and st.session_state.excel_data is not None:
        
        user_input = st.chat_input("Ask about the data:")
        table_name = 'TRANSACTION1'
        columns = get_table_columns(cursor, table_name)

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display the user message
            with st.chat_message("user"):
                st.markdown(user_input)

            # Get the chatbot's response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # If the user wants to exit, end the chat
                if "exit" in user_input.lower() or "thank you" in user_input.lower():
                    st.session_state.messages.append({"role": "assistant", "content": "Goodbye! Feel free to come back anytime."})
                    full_response = 'Goodbye! Feel free to come back anytime'
                    message_placeholder.markdown(full_response)
                    st.stop()  # Stop the app from further execution

                # Get the chatbot's response based on the Excel data
                full_response = get_bot_response(cursor, table_name, user_input, columns, st.session_state.excel_data)

                # Update the response in the chat
                message_placeholder.markdown(full_response)

            # Append assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    else:
        st.info("Please upload an Excel file to start chatting with the bot.")

if __name__ == "__main__":
    main()
