# TUnit
---
Time unit types. For transparency, safety and readability.

## Examples:

```python
from tunit import Days, Hours, Minutes, Seconds, Milliseconds

# Type annotations:
def timestamp() -> Milliseconds:
    # Time unit conversions:
    return Milliseconds(Seconds(1))  # 1_000 ms

# Converting to smaller units:
assert Hours(Days(1)) == Hours(24) == 24

# Converting to bigger units:
assert Minutes(Seconds(65)) == Minutes(1) == 1

# Converting floats to time units:
assert Seconds(Minutes(0.5)) == 0  # Time units hold integers!
assert Seconds.fromRawUnit(Minutes, 0.5) == 500  # Better approach when fractions matter!
```

## License
MIT
