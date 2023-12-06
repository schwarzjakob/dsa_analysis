
import requests
import json

# Set the login endpoint URL
url = "https://app.roll20.net/v2/sessions/create"
chatlog = 'https://app.roll20.net/campaigns/chatarchive/6821565'
filename = 'chatlog.txt'


# Set the request headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Set the login credentials
username = "jakob.schwarz97@gmail.com"
password = "happyifWEare42"

# Set the request body
data = {
    "email": username,
    "password": password
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response content
print(response.content)

