import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import os
import json

@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()   
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}." 

@function_tool()
async def search_web(
    context: RunContext, 
    query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."    


@function_tool()
async def save_unanswered_question(
    context: RunContext, 
    question: str
) -> str:
    """
    Saves a question to a JSON file if the answer is not found in the provided data.
    """
    try:
        file_path = "unanswered_questions.json"
        questions = []
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r") as f:
                questions = json.load(f)
        
        questions.append({"question": question})
        
        with open(file_path, "w") as f:
            json.dump(questions, f, indent=4)
            
        logging.info(f"Saved unanswered question: {question}")
        return f"Question saved to unanswered_questions.json"
    except Exception as e:
        logging.error(f"Error saving unanswered question: {e}")
        return f"An error occurred while saving the question."