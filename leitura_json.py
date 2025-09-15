import json

with open('teste.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


objs = []
for obj in data:
    objs.append(obj)
