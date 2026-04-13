import requests

API_KEY = "d1201b91c8db87a660753964e8878625"

ville = input("Entrez le nom d'une ville : ")

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": ville,
    "appid": API_KEY,
    "units": "metric",
    "lang": "fr"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Ville :", data["name"])
    print("Température :", data["main"]["temp"], "°C")
    print("Météo :", data["weather"][0]["description"])
else:
    print("Erreur :", response.status_code)