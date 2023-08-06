qstrbuilder: convert Python objects to a KDB+q string
=======================

Usage Example:

```
import datetime as dt
from qstrbuilder import build
build("Hello", 3., [3., dt.date(2000, 1, 1)], [], {"A": 3, "B": 4})
```
