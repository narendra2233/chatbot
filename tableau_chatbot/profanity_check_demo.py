from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from better_profanity import profanity
import re
import scrubadub
from redact import redact
import openai

load_dotenv()
llm=ChatOpenAI(model='gpt-4o-mini')
prompt=ChatPromptTemplate([
    ('system','you are translation assistant')
    ,('user','{text}')
])

chain=prompt | llm

result=chain.invoke({
    'text':'i kill you in hindi'
})

response=result.content
"""#def privacy_check(text):
    redacted_text = redact(text)
    return redacted_text"""
if profanity.contains_profanity(response):
    print("profanity detected")
    response_clean=re.sub(r'[^\w\s]', '', response)
    sanitized_text=profanity.censor(response_clean)
    print("sanitized text: ",sanitized_text)
    #result=privacy_check(sanitized_text)
    #print(result)
    
else:
    print("no profanity")
    
    



