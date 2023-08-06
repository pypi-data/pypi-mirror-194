# Examples

---

## Iterating through components

???+ info

    automatic pagination

This example shows how to iterate through components, requesting 32 components
from the database at a time:

```py
import itkdb

client = itkdb.Client()
for i, comp in client.get(
    "listComponents", json={"project": "P", "pageInfo": {"pageSize": 32}}
)

for i, comp in enumerate(comps):
    print(i, comp["code"])
```
