# Copyright (c) 2025 TOON Format Organization
# SPDX-License-Identifier: MIT
"""JSON interop helpers for TOON.

Convenience wrappers for working directly with JSON strings. Data often arrives
as raw JSON text -- LLM tool outputs, REST API responses, log files -- where the
JSON `null` keyword has no direct TOON equivalent and must become Python `None`
before encoding.

`encode()` already renders `None` as the TOON `null` literal, and the standard
library's `json.loads` already maps `null` to `None`, so these helpers simply
remove the boilerplate of wiring the two together for the common
JSON-string -> TOON path.
"""

import json
from typing import Any, Optional

from .encoder import encode
from .types import EncodeOptions, JsonValue

__all__ = ["loads", "encode_json"]


def loads(json_string: str, **kwargs: Any) -> JsonValue:
    """Parse a JSON string into TOON-ready Python objects.

    A thin wrapper around :func:`json.loads`. JSON `null` becomes Python `None`,
    `true`/`false` become `bool`, objects become `dict`, and arrays become
    `list` -- exactly the types that :func:`~toon_format.encode` expects.

    Args:
        json_string: The JSON text to parse.
        **kwargs: Additional keyword arguments forwarded to ``json.loads``
            (e.g. ``parse_float``).

    Returns:
        The parsed Python value.

    Raises:
        json.JSONDecodeError: If ``json_string`` is not valid JSON.

    Example:
        >>> from toon_format import loads
        >>> loads('{"a": null, "b": [1, null, 3]}')
        {'a': None, 'b': [1, None, 3]}
    """
    return json.loads(json_string, **kwargs)


def encode_json(json_string: str, options: Optional[EncodeOptions] = None) -> str:
    """Encode a JSON string directly into TOON format.

    Equivalent to ``encode(loads(json_string), options)``. Use this when data
    arrives as raw JSON text and you want TOON out in a single call -- JSON
    `null` is handled as `None` automatically, with no manual preprocessing.

    Args:
        json_string: The JSON text to convert.
        options: Optional encoding options (see
            :class:`~toon_format.EncodeOptions`).

    Returns:
        The TOON-formatted string.

    Raises:
        json.JSONDecodeError: If ``json_string`` is not valid JSON.

    Example:
        >>> from toon_format import encode_json
        >>> print(encode_json('{"name": "Alice", "mood": null}'))
        name: Alice
        mood: null
    """
    return encode(loads(json_string), options)
