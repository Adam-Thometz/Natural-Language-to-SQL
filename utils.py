import openai

def create_table_definition(df):
    definition = f"""
    ### sqlite SQL table, with its properties:
    # 
    # instruments({",".join(str(col) for col in df.columns)})
    """

    return definition

def create_prompt(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer: {query_prompt}\nSELECT"
    messages = [
        {"role": "system", "content": "You create SQL queries based on given table information and a user prompt"},
        {"role": "user", "content": definition + query_init_string}
    ]
    return messages

def call_openai(query_result):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=query_result,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['#', ';']
    )

    query = response['choices'][0]['message']['content']
    if not query.startswith("SELECT"):
        query = "SELECT"+query
    return query

# Prompt could look like this: 

### sqlite SQL table, with its properties:
# 
# instruments(name,instrument_family,made_from,how_to_play,is_rhythm,video_uri)
# "### A query to answer: show all rhythmic instruments
# SELECT...