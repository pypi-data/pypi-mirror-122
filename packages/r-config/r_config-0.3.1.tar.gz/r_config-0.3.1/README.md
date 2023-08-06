# r_config

Standard way that I am using to use config

## usage:

#### from str:

```python
from r_config import RConfig

r_config = RConfig()

str_yaml = """
    yek:
      ramin: 2
      mehran: 'salam'
    # comment to test
    dow:
      se:
        p1: 2.2
      f1: 'khodafez'
"""

r_config.update_from_str(str_yaml)

```

#### from file:

```python
from r_config import RConfig
from pathlib import Path

r_config = RConfig()

path = Path('/path/to/config.yaml')

r_config.update_from_file(path)

```