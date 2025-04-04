from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
load_dotenv()
llm=ChatOpenAI(model='gpt-4o-mini')
prompt=ChatPromptTemplate.from_messages(
    [
        ('system','you are helpful assistant'),MessagesPlaceholder(variable_name="messages")
    ]
)
store={}

def get_session_history(session_id : str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]
config={"configurable":{"session_id":"first"}}
model_with_memory=RunnableWithMessageHistory(llm,get_session_history)   

chain=prompt | llm | StrOutputParser()

print(chain.invoke({'messages':[HumanMessage(content="Hi I am Narendra")]}) ) #pass list

print(chain.invoke({'messages':["Narendra is my name"]}))

print(model_with_memory.invoke({'mesages':["what is my name?"]},config=config).content)

print(model_with_memory.invoke([HumanMessage(content="what is my name?")],config=config).content)
