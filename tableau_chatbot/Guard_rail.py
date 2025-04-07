import os
from dotenv import load_dotenv
import openai
from guardrails import Guard

load_dotenv()

#guard=Guard()

def get_openai_response():
    response=openai.chat.completions.create(model='gpt-4',
                                            messages=[{'role':'user','content':'how many moons does jupitor have?'}]
                                            )
    return response.choices[0].message.content

def validate_with_guardrail(response):
    result=guardrail(
        messages=[{'role':'user','content':response}],
        model='gpt-4'

    )
    return result.validated_output

response=get_openai_response()

print("original response",response)

validated_response = validate_with_guardrail(response)
print("Validated Response:", validated_response)


