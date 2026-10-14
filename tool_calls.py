import json

def extract_tool_call(data: dict) -> dict | None:
    message = data['choices'][0]['message']

    tool_calls = message.get('tool_calls')
    if not tool_calls:
        return None
    
    tool_function = tool_calls[0]['function']
    tool_name = tool_function['name']
    args = json.loads(tool_function['arguments']) 
    return {'tool': tool_name, 'args': args}
