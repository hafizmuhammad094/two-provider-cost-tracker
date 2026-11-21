# Two-Provider LLM Cost Tracker

## Project Description
This Python project sends the same prompt to Google Gemini and Groq APIs and compares their responses.

## Features
- Connects to two AI providers.
- Measures response time.
- Retrieves actual input and output tokens.
- Calculates estimated API cost.
- Saves results in results.json.

## Technologies
- Python
- Google Gemini API
- Groq API
- uv
- python-dotenv

## Installation
1. Clone the repository.
2. Run `uv sync`.
3. Create a `.env` file using `.env.example`.
4. Add your API keys to `.env`.

## Run the Project

```bash
uv run tracker.py "What is Artificial Intelligence?"
```

## Output
The program displays provider responses and a comparison table. Results are saved in results.json.

## What I Learned
I learned how to connect multiple LLM APIs, retrieve token usage, measure response time, and calculate estimated API costs.
