import json


def parse_tool_call(text: str) -> dict:
    """Extract a tool call from a raw model reply.

    Returns {"tool": str, "args": dict}.
    Raises ValueError for any reply we cannot trust.
    """
    # Step 1: locate the JSON object inside the surrounding text.
    start = text.find("{")
    end = text.rfind("}")

    # Step 2: no braces, or braces in the wrong order -> no JSON at all.
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model reply")

    # Step 3: cut out only the JSON part.
    candidate = text[start:end + 1]

    # Step 4: parse it. Convert the library error into our own error type.
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as err:
        raise ValueError(f"Broken JSON in model reply: {err}") from err

    # Step 5: validate the shape.
    if not isinstance(data, dict):
        raise ValueError("JSON is not an object")
    if "tool" not in data:
        raise ValueError("JSON has no 'tool' key")

    args = data.get("args", {})
    if not isinstance(args, dict):
        raise ValueError("'args' must be an object")

    return {"tool": data['tool'], "args": args}


# --- Tests ---------------------------------------------------------------

""" # Test 1: clean JSON
result = parse_tool_call('{"tool": "search", "args": {"query": "apoBank"}}')
assert result == {"tool": "search", "args": {"query": "apoBank"}}

# Test 2: JSON surrounded by extra text
result = parse_tool_call(
    'Sure! Here is the call: {"tool": "search", "args": {"query": "apoBank"}} Done.'
)
assert result["tool"] == "search"
assert result["args"]["query"] == "apoBank"

# Test 3: broken JSON must raise ValueError
try:
    parse_tool_call('{"tool": "search", "args": ')
    assert False, "Expected ValueError"
except ValueError:
    pass

try:
    parse_tool_call("I don't know")
    assert False, "Expect ValueError"
except ValueError:
    pass

try:
    parse_tool_call("{'tool': 'search', 'args': 'apoBank'}")
    assert False, 'Expected ValueError'
except ValueError:
    pass

try:
    parse_tool_call('{"tool": "search", "args": "apoBank"}')
    assert False, 'Expected ValueError'
except ValueError:
    pass

print("All tests passed") """