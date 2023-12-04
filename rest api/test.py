import requests
endpoint = "hello"

post_response = requests.post("http://127.0.0.1:5000/" + endpoint)
get_response = requests.get("http://127.0.0.1:5000/" + endpoint + "/dadson")

print(get_response.json())