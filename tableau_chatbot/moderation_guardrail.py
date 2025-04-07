import openai
from dotenv import load_dotenv 
import os


# Load environment variables from .env file
load_dotenv()



def generate_response(prompt):
    # Step 1: Generate the LLM response
    response = openai.chat.completions.create(
        model="gpt-4",  # Or use "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return response.choices[0].message.content

def check_moderation(text):
    # Step 2: Check response with Moderation API
    moderation_response = openai.Moderation.create(input=text)
    
    if moderation_response['results'][0]['flagged']:
        print("Response flagged. Requesting a new response...")
        return True
    else:
        print("Response is clean.")
        return False

def get_safe_response(prompt, max_retries=3):
    attempts = 0
    while attempts < max_retries:
        # Generate response from the LLM
        response = generate_response(prompt)
        
        # Check if the response is flagged
        if check_moderation(response):
            attempts += 1
            print(f"Attempt {attempts}: Flagged. Retrying...")
        else:
            return response  # Safe response, return it immediately
        
    # After max retries, return a message
    return "Sorry, I couldn't generate a safe response. Please try again later."

# Example usage
prompt = "Tell me a joke about politics."
safe_response = get_safe_response(prompt)
print("Final Response:", safe_response)
