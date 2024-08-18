# Text-to-SQL with LangChain and OpenAI

This project provides a Gradio-based web application that allows users to interact with an SQLite database using natural language queries. It leverages the LangChain library and OpenAI's language model to convert plain English questions into SQL queries and execute them on the provided database.

Try the app: https://sabagul-text-to-sql.hf.space/

![Alt text](tts.png)


## Features

- **Upload SQLite Database**: Upload an SQLite database file to the application.
- **Natural Language Queries**: Enter plain English queries to retrieve data from the database.
- **Real-time Results**: Get results from your database based on your queries.

## Installation

To set up and run this application locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/Saba-Gul/Text-to-SQL.git
cd text-to-sql
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Run the Application

```bash
python app.py
```

## Deployment

This application can be deployed on Hugging Face Spaces or any other platform that supports Python and environment variables.

### Hugging Face Spaces Deployment

1. **Create a New Space**: Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new space.
2. **Add Secrets**: In your space settings, add a secret named `OPENAI_API_KEY` with your OpenAI API key as the value.
3. **Upload Code**: Push your code to the repository connected to your Hugging Face Space.

## Usage

1. **Open the Application**: Navigate to the URL provided by your Hugging Face Space or local server.
2. **Upload Database**: Use the file upload component to upload an SQLite database file.
3. **Query the Database**: Enter your SQL query in plain English and click "Run Query" to see the results.

## Example Queries

- "How many rows are there?"
- "What is the total revenue by month?"
- "Which product line had the largest revenue?"
- "Which day of the week has the best average ratings for each branch?"

