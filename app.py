import os
import gradio as gr
import sqlite3
from langchain.llms import OpenAI
from langchain_community.utilities import SQLDatabase
#from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# Fetch the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('openai')
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key is not set in environment variables.")

# Set the OpenAI API key for the OpenAI library
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
#os.environ("openai")
# Set your OpenAI API key (replace 'your-openai-api-key-here' with your actual key)


# Global variable to store the database path
db_path = None

# Function to upload and set the SQLite database
def upload_database(db_file):
    global db_path
    db_path = db_file.name  # Get the path of the uploaded file
    return f"Database {db_file.name} uploaded successfully!"

# Function to run the LangChain SQL queries
def query_sql_db(query):
    if db_path is None:
        return "Please upload an SQLite database file first."

    try:
        # Connect to the uploaded SQLite database
        input_db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        # Create an instance of the OpenAI model
        openai_llm = OpenAI()
        
        # Use the LLM instance in the SQLDatabaseChain
        db_chain = SQLDatabaseChain.from_llm(openai_llm, input_db, verbose=False)
        
        # Execute the query
        result = db_chain.run(query)
        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create a Gradio interface for both file upload and query
with gr.Blocks() as iface:
    gr.Markdown("# Text-to-SQL")
    gr.Markdown("Upload your SQLite database and then type a question in plain English to get the SQL query result.")

    # File upload component
    db_file = gr.File(label="Upload SQLite Database", file_types=[".sqlite", ".db"])
    upload_btn = gr.Button("Upload Database")
    upload_output = gr.Textbox(label="Upload Status")

    # Input for querying the database
    query_input = gr.Textbox(label="Enter your query in plain English")
    query_output = gr.Textbox(label="SQL Query Result")
    query_btn = gr.Button("Run Query")

    # Link the upload button to the upload_database function
    upload_btn.click(upload_database, inputs=db_file, outputs=upload_output)
    
    # Link the query button to the query_sql_db function
    query_btn.click(query_sql_db, inputs=query_input, outputs=query_output)

# Launch the app
iface.launch()
