import os
import openai
import pandas as pd

from secret import API_KEY
from sqlalchemy import create_engine, text
from utils import create_prompt, call_openai

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

EXIT_KEY = "q"
ERROR_MESSAGE = "Sorry, no results 🤷🏼‍♂️"

df = pd.read_json("instruments.json")
# TEMP DATABASE IN RAM
temp_db = create_engine("sqlite:///:memory:")
# PUSH PANDAS DF ---> TEMP DB
df.to_sql(name="instruments", con=temp_db)

user_input = ""
while user_input != EXIT_KEY:
    print("Enter a prompt. Enter q to quit")
    user_input = input()
    if user_input != EXIT_KEY:
        query_result = create_prompt(df, user_input) # DF + query that does ...
        response = call_openai(query_result)
        print(f"Query: {response}")

        with temp_db.connect() as conn:
            result = conn.execute(text(response))

        print("Results: *")
        print("**********")
        returned_data = result.all()
        for i, instrument in enumerate(returned_data):
            print(f"{i+1}. {instrument.name.lower().capitalize()}")
        print("**********")
print("Bye!")

# HOW TO PICK A LANGUAGE MODEL
# Think about cost of the model and how often you'll use it
# How many tokens you'll pass into the model or get back
# Importance of accuracy in results

# OpenAI Completion Call Params
# model (i.e. text-davinci-003, etc.)
# prompt
# temperature (0.0 to 1.0, the higher, the more likely the model will take risks and be creative)
# max_tokens (most tokens to use in response)
# top_p (similar to temperature)
# n (how many completions to generate)
# frequency_penalty (-2.0 to 2.0, likelihood of model repeating itself, higher means less likely, 0.1 to 1.0 is usually good enough)
# presence_penalty (-2.0 to 2.0, similar to frequency_penalty)