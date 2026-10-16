SEARCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search the web for recent news on a topic.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."}
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}


def search(query: str) -> str:
    """
    Search the web for recent news on a topic.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    headline1 = f"Alphabet Inc. (Google's parent company) has 190,820 full-time employees worldwide as of December 31, 2025"
    return f"Search results for {query} : {headline1}"


TOOL_FUNCTIONS = {"search": search}
