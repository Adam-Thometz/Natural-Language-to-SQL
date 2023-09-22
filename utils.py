import openai

def create_table_definition(df):
    prompt = """
    ### sqlite SQL table, with its properties:
    # 
    # instruments({})
    # 
    """.format(",".join(str(col) for col in df.columns))

    return prompt

def create_prompt(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer: {query_prompt}\nSELECT"
    return definition + query_init_string

def call_openai(query_result):
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
    query = response['choices'][0]['text']
    if query.startswith(" "):
        query = "SELECT"+query
    return query

# Prompt could look like this: 

### sqlite SQL table, with its properties:
# 
# instruments(name,instrument_family,made_from,how_to_play,is_rhythm,video_uri)
# "### A query to answer: show all rhythmic instruments
# SELECT...