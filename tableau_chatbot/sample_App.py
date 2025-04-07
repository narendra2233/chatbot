import openai
import streamlit as st
import pandas as pd
import io
from dotenv import load_dotenv
import sqlite3
import os
from nemoguardrails import RailsConfig,LLMRails
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails




def get_bot_response(text,messages):
    load_dotenv()
    llm=ChatOpenAI(model='gpt-4o-mini')
    prompt = ChatPromptTemplate.from_messages([
    ('system', 'you are a helpful assistant'),
    MessagesPlaceholder("history"),
    ('user', '{text}')
])

    config=RailsConfig.from_path("config2")
    guardrail=RunnableRails(config=config)
    chain=prompt | llm | StrOutputParser()
    guardrail_chain=guardrail | chain

    result=guardrail_chain.invoke({'history':[('user',"i am from bangalore")],'text':text})
    return result

 
    

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

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Get user input after file is uploaded
    
    user_input = st.chat_input("Ask about the data:")
    
    if user_input:
            st.session_state.messages.append({'role':'user','content':user_input})

            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                if "exit" in user_input.lower() or "thank you" in user_input.lower():
                    st.session_state.messages.append({"role": "assistant", "content": "Goodbye! Feel free to come back anytime."})
                    full_response = 'Goodbye! Feel free to come back anytime'
                    message_placeholder.markdown(full_response)
                    st.stop()  # Stop the app from further execution
                full_response=get_bot_response(user_input,st.session_state.messages)
                message_placeholder.markdown(full_response)

            st.session_state.messages.append({'role':'assistant','content':full_response})

if __name__ == "__main__":
    main()