# Natural Language to SQL Converter

A simple natural language to SQL converter

## Tech Stack
- Python
- Pandas
- OpenAI API
- SQLAlchemy / SQLite

## How it works

1. Pandas converts the data file (in this case, `instruments.json`) into a data frame
2. A temporary SQLite database is created using SQLAlchemy and the data frame is pushed to the database
3. Your request from the `user_input` variable is converted into a usable prompt
4. The prompt is sent to OpenAI's Completion API
5. Grab the resulting query and run it in the database


## How to run on machine
1. Get an API key from OpenAI, and place it in a file called `secret.py` in the root
2. You can replace the data if you wish. [Check the Pandas docs to see supported files.](https://pandas.pydata.org/docs/user_guide/io.html)
3. Create a virtual environment by running `python3 -m venv env`
4. Start the environment by running `source env/bin/activate`
5. Run `pip install -r requirements.txt` to install dependencies
6. Run at anytime by running `python3 app.py`