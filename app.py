import os
import gradio as gr
from langchain.llms import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# Fetch the OpenAI API key
OPENAI_API_KEY = os.getenv("openai")
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key is not set in environment variables.")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Global variable to store database path
db_path = None


# ---------- SQL SAFETY LAYER ----------
def is_safe_sql(sql: str) -> bool:
    forbidden_keywords = ["drop", "delete", "update", "insert", "alter"]
    sql_lower = sql.lower()
    return not any(keyword in sql_lower for keyword in forbidden_keywords)


# ---------- DATABASE UPLOAD ----------
def upload_database(db_file):
    global db_path
    db_path = db_file.name
    return f"Database '{db_file.name}' uploaded successfully."


# ---------- QUERY EXECUTION ----------
def query_sql_db(query):
    if db_path is None:
        return "❌ Please upload an SQLite database first."

    try:
        # Load database
        input_db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

        # Initialize LLM
        llm = OpenAI(temperature=0)

        # Create SQL chain with intermediate steps
        db_chain = SQLDatabaseChain.from_llm(
            llm,
            input_db,
            verbose=False,
            return_intermediate_steps=True
        )

        # Run chain
        response = db_chain(query)

        # Extract generated SQL
        generated_sql = response["intermediate_steps"][0]

        # Validate SQL
        if not is_safe_sql(generated_sql):
            return f"❌ Unsafe SQL detected and blocked:\n\n{generated_sql}"

        # Execute safe SQL
        result = response["result"]

        return (
            f"✅ Generated SQL:\n{generated_sql}\n\n"
            f"📊 Query Result:\n{result}"
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ---------- GRADIO UI ----------
with gr.Blocks() as iface:
    gr.Markdown("# 🧾 Text-to-SQL Analytics Assistant")
    gr.Markdown(
        "Upload a SQLite database and ask questions in plain English. "
        "The system converts them into SQL queries and executes them safely."
    )

    db_file = gr.File(label="Upload SQLite Database", file_types=[".sqlite", ".db"])
    upload_btn = gr.Button("Upload Database")
    upload_output = gr.Textbox(label="Upload Status")

    query_input = gr.Textbox(label="Ask a question (Natural Language)")
    query_output = gr.Textbox(label="Result")
    query_btn = gr.Button("Run Query")

    upload_btn.click(upload_database, inputs=db_file, outputs=upload_output)
    query_btn.click(query_sql_db, inputs=query_input, outputs=query_output)

iface.launch()
