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
    headline1 = f"1. apoBank reports stable Q3 results. 2. apoBank launches new app for medical practices. 3. apoBank expands advisory for young doctors."
    return f"Search results for {query}: {headline1}"


TOOL_FUNCTIONS = {"search": search}
