import pytest
from tool_calls import extract_tool_call


def test_tool_call_response_with_right_dict():
    result = extract_tool_call(
        {
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_JURA0cNaXWXR6SHJPoi5n35l",
                                "type": "function",
                                "function": {
                                    "name": "search",
                                    "arguments": (
                                        '{"query":"Google number of employees 2026"}'
                                    ),
                                },
                            }
                        ],
                        "refusal": None,
                        "annotations": [],
                    },
                    "logprobs": None,
                    "finish_reason": "tool_calls",
                }
            ],
        }
    )

    assert result == {
        "tool": "search",
        "args": {"query": "Google number of employees 2026"},
    }


def test_tool_call_response_without_tool_calls():
    response = {
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "refusal": None,
                    "annotations": [],
                },
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
    }

    result = extract_tool_call(response)
    assert result == None

def test_tool_call_response_with_tool_calls_is_none():
    response = {
        "choices": [
            {
                 "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "refusal": None,
                    "annotations": [],
                    "tool_calls": None
                },
                "logprobs": None,
                "finish_reason": "tool_calls",
            }
        ],
    }
    result = extract_tool_call(response)
    assert result == None

def test_tool_call_response_with_broken_json():
    response = {
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "refusal": None,
                    "annotations": [],
                    "tool_calls": [
                        {
                            "id": "call_test",
                            "type": "function",
                            "function": {
                                "name": "search",
                                "arguments": '{"query": "Google",}',
                            },
                        }
                    ],
                },
                "logprobs": None,
                "finish_reason": "tool_calls",
            }
        ],
    }
    with pytest.raises(ValueError, match="Illegal trailing comma"):
        extract_tool_call(response)
