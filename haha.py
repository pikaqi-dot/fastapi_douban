import json
a = '{"a:1", "b:1"}'
c=json.loads(a)
print(c, type(c))
