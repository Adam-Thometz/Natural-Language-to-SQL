import os
import openai
import pandas as pd

from secret import API_KEY
from sqlalchemy import create_engine, text
from utils import combine_prompts, handle_response

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

df = pd.read_json("instruments.json")

# TEMP DATABASE IN RAM
temp_db = create_engine("sqlite:///:memory:")
# PUSH PANDAS DF ---> TEMP DB
df.to_sql(name="instruments", con=temp_db)

# SQL query on TEMP DB
# with temp_db.connect() as conn:
    # makes connection
    # run code in indentation/block
    # result = conn.execute(text("SELECT * FROM instruments"))
    # print(result.all())
    # auto close connection


user_input = "show all rhythmic instruments" # NL
query_result = combine_prompts(df, user_input) # DF + query that does ... + NLP
# print(query_result)

response = openai.Completion.create(
    model='text-davinci-002',
    prompt=query_result,
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['#', ';']
)
# print("API response", response)
# print("handled response", handle_response(response))

with temp_db.connect() as conn:
    query = handle_response(response)
    result = conn.execute(text(query))

print("results", result.all())

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