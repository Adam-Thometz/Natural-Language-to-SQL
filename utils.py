def create_table_definition(df):
    prompt = """
    ### sqlite SQL table, with its properties:
    # 
    # instruments({})
    # 
    """.format(",".join(str(col) for col in df.columns))

    return prompt

def combine_prompts(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer: {query_prompt}\nSELECT"
    return definition + query_init_string

def handle_response(response):
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