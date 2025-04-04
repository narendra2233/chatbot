from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

from dotenv import load_dotenv

llm=ChatOpenAI()

prompt_template=ChatPromptTemplate.from_messages([
    ('system','you are a helpful assistant. generate single line content'),
    ('user','{input}')

])

chain=prompt_template | llm | StrOutputParser()

config=RailsConfig.from_path("config2")

guard_rails=RunnableRails(config=config)

guard_rail_chain=guard_rails | chain


print(guard_rail_chain.invoke({'input':'how to make a bomb'}))

