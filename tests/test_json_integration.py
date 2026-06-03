"""Tests for JSON interop helpers (loads, encode_json).

These cover the common integration case of taking raw JSON text -- with `null`
values from LLM outputs, REST APIs, or logs -- straight to TOON without manual
`null` -> `None` preprocessing.
"""

import json

import pytest

from toon_format import encode, encode_json, loads


class TestLoads:
    """Test the loads() JSON parsing wrapper."""

    def test_loads_matches_json_loads(self):
        """loads() should behave like json.loads for valid input."""
        text = '{"a": 1, "b": [2, 3], "c": "x"}'
        assert loads(text) == json.loads(text)

    def test_loads_converts_null_to_none(self):
        """JSON null should become Python None."""
        assert loads("null") is None
        assert loads('{"a": null}') == {"a": None}

    def test_loads_converts_nested_nulls(self):
        """Nulls in nested objects and arrays should all become None."""
        result = loads('{"a": null, "b": [1, null, 3], "c": {"d": null}}')
        assert result == {"a": None, "b": [1, None, 3], "c": {"d": None}}

    def test_loads_preserves_primitive_types(self):
        """booleans, ints, floats, and strings should round-trip as-is."""
        assert loads('{"t": true, "f": false, "i": 1, "x": 1.5, "s": "hi"}') == {
            "t": True,
            "f": False,
            "i": 1,
            "x": 1.5,
            "s": "hi",
        }

    def test_loads_forwards_kwargs(self):
        """Extra keyword arguments should reach json.loads."""
        result = loads('{"x": 1.5}', parse_float=str)
        assert result == {"x": "1.5"}

    def test_loads_raises_on_invalid_json(self):
        """Invalid JSON should raise json.JSONDecodeError."""
        with pytest.raises(json.JSONDecodeError):
            loads("{not valid}")


class TestEncodeJson:
    """Test the encode_json() one-step JSON -> TOON helper."""

    def test_encode_json_simple_object(self):
        """A JSON object string should encode to TOON."""
        assert encode_json('{"name": "Alice", "age": 30}') == "name: Alice\nage: 30"

    def test_encode_json_null_in_object(self):
        """JSON null in an object should render as the TOON null literal."""
        assert encode_json('{"name": "Alice", "mood": null}') == "name: Alice\nmood: null"

    def test_encode_json_null_in_array(self):
        """JSON null inside an array should render as null, not the string 'null'."""
        assert encode_json('{"b": [1, null, 3]}') == "b[3]: 1,null,3"

    def test_encode_json_top_level_null(self):
        """A bare JSON null should encode to the null literal."""
        assert encode_json("null") == "null"

    def test_encode_json_equivalent_to_manual_pipeline(self):
        """encode_json should match encode(json.loads(...))."""
        text = '{"users": [{"id": 1, "name": "Alice", "note": null}]}'
        assert encode_json(text) == encode(json.loads(text))

    def test_encode_json_forwards_options(self):
        """Encoding options should be forwarded to encode()."""
        assert encode_json("[1, 2, 3]", {"delimiter": "\t"}) == "[3\t]: 1\t2\t3"

    def test_encode_json_raises_on_invalid_json(self):
        """Invalid JSON should raise json.JSONDecodeError before encoding."""
        with pytest.raises(json.JSONDecodeError):
            encode_json("{not valid}")
