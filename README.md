# pogo-tier-list

PokemonGo Attacker Tier List parser.

Attempting to use LLM's to give Pokemon Go attacker recommendations.

[Instructor](https://github.com/jxnl/instructor) library is being finicky with these errors:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Pokemon
  Invalid JSON: key must be a string at line 5 column 5 [type=json_invalid, input_value='{\n  "tier": "S Tier",\n...ent fields here\n  }\n}', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/json_invalid
```