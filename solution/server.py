

import requests

url = "http://localhost:8000/characters"
headers = {'Content-type': 'application/json'}


response = requests.get(url)
print(response.json())

personaje = {
    "name":"Gandalf",
    "level":10,
    "role":"Wizard",
    "charisma":15,
    "strenght":10,
    "dexterity":10
}
response = requests.post(url, json=personaje, headers=headers)
print(response.json())

response = requests.get(url)
print(response.json())


personaje_edit = {
    "charisma":20,
    "strenght":15,
    "dexterity":10
}
response = requests.put(url+"/1", json=personaje_edit, headers=headers)
print(response.json())


response = requests.get(url)
print(response.json())



response = requests.delete(url + "/1")
print(response.json())


response = requests.get(url)
print(response.json())














