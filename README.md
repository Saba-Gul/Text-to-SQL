# Natural Language to SQL Analytics Assistant

## Problem
Business users often need insights from databases but cannot write SQL queries.

## Solution
This project implements a Text-to-SQL analytics assistant that converts natural language
questions into SQL queries and executes them on a relational database.

## How It Works
1. User enters a question in plain English
2. An LLM-based SQL agent converts the question into SQL
3. The SQL query is executed on a SQLite database
4. Results are returned to the user

## Tech Stack
- Python
- LangChain
- OpenAI
- SQLite

## Use Cases
- Self-serve analytics
- Business intelligence
- Natural language data exploration
