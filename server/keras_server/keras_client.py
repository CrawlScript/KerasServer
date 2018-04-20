#coding=utf-8
import requests
import json
import numpy as np
base_url = "http://127.0.0.1:5000"

data = {
    "features": np.random.randn(5,10).tolist()
}
params = {
    "data": json.dumps(data)
}

# print(data)


for i in range(100):
    content = requests.get(base_url, params).content
    print(content)