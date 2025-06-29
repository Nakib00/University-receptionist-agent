import json
from livekit.agents import function_tool, RunContext
from tools import save_unanswered_question
from university_data import university_data

def search_data(data, query):
    if isinstance(data, dict):
        for key, value in data.items():
            if query in str(key).lower() or query in str(value).lower():
                return data
            result = search_data(value, query)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            if query in str(item).lower():
                return item
            result = search_data(item, query)
            if result:
                return result
    return None

@function_tool()
async def get_university_info(
    context: RunContext,
    question: str
) -> str:
    """
    Get information about the university from the knowledge base.
    If the answer is not found, the question is logged.
    """
    query_parts = question.lower().split()
    for part in query_parts:
        result = search_data(university_data, part)
        if result:
            return json.dumps(result, indent=2)

    await save_unanswered_question(context, question=question)
    return "I could not find the answer in my current knowledge base. I have logged your question for future improvements."