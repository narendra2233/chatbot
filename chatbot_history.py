from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage
load_dotenv()

prompt=ChatPromptTemplate.from_messages([
    ('system','you are a helpful assistant. please respond to the queries'),
    ('user','Question: {Question}')
])

llm=ChatOpenAI(model='gpt-4o-mini')
output_parser=StrOutputParser()

prompt_template=prompt.format(Question="Hi")

print(llm.invoke(prompt_template).content)

store={}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model_with_memory=RunnableWithMessageHistory(llm,get_session_history)

config={"configurable":{"session_id":"first_chat"}}

print(model_with_memory.invoke([HumanMessage(content="Hi I am Narendra")],config=config).content)

print(store)