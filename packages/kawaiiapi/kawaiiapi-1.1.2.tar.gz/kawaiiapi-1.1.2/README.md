# kawaii api
The kawaii api from Error44 as python package 

```python
import kawaiiapi

api = kawaiiapi.Kawaii("token")

await api.endpoints("gif")

await api.get("gif", "kiss")
```