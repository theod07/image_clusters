import requests
import time
import json

with open('/Users/wonder/.insta.json', 'r') as f:
    TOKEN = json.load(f)['access_token']

url = 'https://api.instagram.com/v1/users/self/?access_token='
# url = 'https://api.instagram.com/v1/users/500934533/?access_token='
data = requests.get(url+TOKEN)
