# TOON Format for Python

[![Tests](https://github.com/toon-format/toon-python/actions/workflows/test.yml/badge.svg)](https://github.com/toon-format/toon-python/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/toon_format.svg)](https://pypi.org/project/toon_format/)

> **⚠️ Beta Status (v0.9.x):** This library is in active development and working towards spec compliance. Beta published to PyPI. API may change before 1.0.0 release.

Compact, human-readable serialization format for LLM contexts with **30-60% token reduction** vs JSON. Combines YAML-like indentation with CSV-like tabular arrays. Working towards full compatibility with the [official TOON specification](https://github.com/toon-format/spec).

**Key Features:** Minimal syntax • Tabular arrays for uniform data • Array length validation • Python 3.8+ • Comprehensive test coverage • Zero runtime dependencies.

```bash
# Beta published to PyPI - install from source:
git clone https://github.com/toon-format/toon-python.git
cd toon-python
uv sync

# Or install directly from GitHub:
pip install git+https://github.com/toon-format/toon-python.git
```

## Quick Start

```python
from toon_format import encode, decode

# Simple object
encode({"name": "Alice", "age": 30})
# name: Alice
# age: 30

# Tabular array (uniform objects)
encode([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
# [2,]{id,name}:
#   1,Alice
#   2,Bob

# Decode back to Python
decode("items[2]: apple,banana")
# {'items': ['apple', 'banana']}
```

## API Reference

### `encode(value, options=None)` → `str`

```python
encode({"id": 123}, {"delimiter": "\t", "indent": 4, "lengthMarker": "#"})
```

**Options:**
- `delimiter`: `","` (default), `"\t"`, `"|"`
- `indent`: Spaces per level (default: `2`)
- `lengthMarker`: `""` (default) or `"#"` to prefix array lengths

### `decode(input_str, options=None)` → `Any`

```python
decode("id: 123", {"indent": 2, "strict": True})
```

**Options:**
- `indent`: Expected indent size (default: `2`)
- `strict`: Validate syntax, lengths, delimiters (default: `True`)

### Working with JSON strings

When data arrives as raw JSON text (LLM tool outputs, REST APIs, logs), skip the
manual `json.loads` step. JSON `null` is handled as `None` automatically.

```python
from toon_format import encode_json, loads

# JSON string straight to TOON
encode_json('{"name": "Alice", "mood": null}')
# name: Alice
# mood: null

# Parse JSON into TOON-ready Python objects (null -> None)
loads('{"b": [1, null, 3]}')
# {'b': [1, None, 3]}
```

`encode_json(json_string, options=None)` is equivalent to `encode(loads(json_string), options)`.

## Format Specification

| Type | Example Input | TOON Output |
|------|---------------|-------------|
| **Object** | `{"name": "Alice", "age": 30}` | `name: Alice`<br>`age: 30` |
| **Primitive Array** | `[1, 2, 3]` | `[3]: 1,2,3` |
| **Tabular Array** | `[{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]` | `[2,]{id,name}:`<br>&nbsp;&nbsp;`1,A`<br>&nbsp;&nbsp;`2,B` |
| **Mixed Array** | `[{"x": 1}, 42, "hi"]` | `[3]:`<br>&nbsp;&nbsp;`- x: 1`<br>&nbsp;&nbsp;`- 42`<br>&nbsp;&nbsp;`- hi` |

**Quoting:** Only when necessary (empty, keywords, numeric strings, whitespace, structural chars, delimiters)

**Type Normalization:** `Infinity/NaN/Functions` → `null` • `Decimal` → `float` • `datetime` → ISO 8601 • `-0` → `0`

## Pydantic Integration – (Structured TOON for LLM Outputs)

Adds a **completely optional** Pydantic integration via the `[pydantic]` extra.

```bash
pip install "toon-python[pydantic]"
```

### Features

- Schema: 50–60 % smaller than model_json_schema()
- Zero JSON parsing errors
- Works with `Instructor`, `Outlines`, `Marvin`, `LangChain agents`, etc.
- Full Pydantic validation preserved

## Usage After Release

```python
from toon_format.pydantic import ToonPydanticModel

class User(ToonPydanticModel):
    name: str
    age: int
    email: str | None = None

# Convert schema to TOON for LLM system prompts
schema_toon = User.schema_to_toon()
# name:str,age:int,email:str|None

# Parse LLM TOON output into validated Pydantic model
toon_output = "name:Ansar,age:25,email:ansar@example.com"
user = User.model_validate_toon(toon_output)

# user.name → "Ansar"
# user.age → 25
# user.email → "ansar@example.com"

# Serialize a model instance back to TOON
toon_str = user.model_dump_toon()
```

## Development

```bash
# Setup (requires uv: https://docs.astral.sh/uv/)
git clone https://github.com/toon-format/toon-python.git
cd toon-python
uv sync

# Run tests (818 tests, 93% coverage, 85% enforced)
uv run pytest --cov=toon_format --cov-report=term

# Code quality
uv run ruff check src/ tests/        # Lint
uv run ruff format src/ tests/       # Format
uv run mypy src/                     # Type check
```

**CI/CD:** GitHub Actions • Python 3.8-3.14 • Coverage enforcement • PR coverage comments

## Project Status & Roadmap

Following semantic versioning towards 1.0.0:

- **v0.8.x** - Initial code set, tests, documentation ✅
- **v0.9.x** - Serializer improvements, spec compliance testing, publishing setup (current)
- **v1.0.0-rc.x** - Release candidates for production readiness
- **v1.0.0** - First stable release with full spec compliance

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

- [📘 Full Documentation](docs/) - Complete guides and references
- [🔧 API Reference](docs/api.md) - Detailed function documentation
- [📋 Format Specification](docs/format.md) - TOON syntax and rules
- [🤖 LLM Integration](docs/llm-integration.md) - Best practices for LLM usage
- [📜 TOON Spec](https://github.com/toon-format/spec) - Official specification
- [🐛 Issues](https://github.com/toon-format/toon-python/issues) - Bug reports and features
- [🤝 Contributing](CONTRIBUTING.md) - Contribution guidelines

## Contributors

- [Xavi Vinaixa](https://github.com/xaviviro)
- [David Pirogov](https://github.com/davidpirogov)
- [Justar](https://github.com/Justar96)
- [Johann Schopplich](https://github.com/johannschopplich)

## License

MIT License – see [LICENSE](LICENSE) for details
