# Stepizer

Chain multiple functions or generators into one pipeline.

Basic use case:
```python
from stepizer import Step


def add_text(string: str) -> str:
    return 'hello, ' + string + '!'


pipeline = Step.chain(
    add_text,
    str.upper,
)

pipeline.run('world')
# HELLO, WORLD!
```
