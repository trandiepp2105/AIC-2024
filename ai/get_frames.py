import requests
import json

hihi = requests.get('http://localhost:8000/api/frames/')

dic = json.loads(hihi.text)

for i in dic:
    print(i)