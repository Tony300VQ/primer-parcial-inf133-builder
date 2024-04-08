

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

personaje = {
    "name":"Robin",
    "level":5,
    "role":"Archer",
    "charisma":10,
    "strenght":15,
    "dexterity":15
}
response = requests.post(url, json=personaje, headers=headers)
print(response.json())
personaje = {
    "name":"Aragorn",
    "level":10,
    "role":"Warrior",
    "charisma":20,
    "strenght":15,
    "dexterity":15
}
response = requests.post(url, json=personaje, headers=headers)
print(response.json())
personaje = {
    "name":"Legolas",
    "level":5,
    "role":"Archer",
    "charisma":15,
    "strenght":10,
    "dexterity":150
}
response = requests.post(url, json=personaje, headers=headers)
print(response.json())

response = requests.get(url)
print(response.json())
response = requests.get(url+"/1")
print(response.json())
print("//////")
response = requests.get(url+"?role=Archer&level=5&charisma=10")
print(response.json())
personaje_edit = {
    "charisma":20,
    "strenght":15,
    "dexterity":15
}
response = requests.put(url+"/2", json=personaje_edit, headers=headers)
print(response.json())

response = requests.get(url)
print(response.json())




response = requests.delete(url + "/3")
print(response.json())


response = requests.get(url)
print(response.json())

print("Others")
personaje = {
    "name":"Aragorn",
    "level":10,
    "role":"Warrior",
    "charisma":20,
    "strenght":15,
    "dexterity":15
}
response = requests.post(url, json=personaje, headers=headers)
print(response.json())
response = requests.get(url)
print(response.json())












