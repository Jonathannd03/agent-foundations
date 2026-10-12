import pytest
from parse_tool_call import parse_tool_call


def test_missing_tool_key_raises():
    with pytest.raises(ValueError, match="JSON has no 'tool' key"):
        parse_tool_call('{"args": {"query": "apoBank2"}}')


def test_clean_json():
    result = parse_tool_call('{"tool": "search", "args": {"query": "apoBank"}}')
    assert result == {"tool": "search", "args": {"query": "apoBank"}}


def test_json_surrounded_by_extra_text():
    result = parse_tool_call(
        'Sure! Here is the call: {"tool": "search", "args": {"query": "apoBank"}} Done.'
    )
    assert result == {"tool": "search", "args": {"query": "apoBank"}}


def test_broken_json():
    with pytest.raises(ValueError, match="Broken JSON in model reply"):
        parse_tool_call('{"tool": "search", "args": }')


def test_reply_without_json_raises():
    with pytest.raises(ValueError, match="No JSON object found in model reply"):
        parse_tool_call("I don't know")


def test_args_not_object_raises():
    with pytest.raises(ValueError, match="'args' must be an object"):
        parse_tool_call('{"tool": "search", "args": "apoBank"} Done')
