from tools import search


def test_search_tool():
    query = f"How many employees does google have?"
    search_reusult = search(query)

    assert query in search_reusult
    assert len(search_reusult) > len(query)
