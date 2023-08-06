## Data

Helps to filter event with contextual data.

```python
import asyncio

from tapp.filters import Data, F

asyncio.run(Data(F.event == {"data": "hello"})({"data": "hello"}))  # True
```
