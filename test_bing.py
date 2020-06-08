import requests

url = "https://microsoft-azure-bing-news-search-v1.p.rapidapi.com/"

querystring = {"Category":"sports"}

headers = {
    'x-rapidapi-host': "microsoft-azure-bing-news-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "2d82bb5d95msh2a4e5c2a45a8eb3p18b00ejsn98308d90b548"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)