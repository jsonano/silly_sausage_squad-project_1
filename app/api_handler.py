from flask import Flask, request, render_template, redirect, url_for, flash, session
import os, urllib.request, json

# Load API keys
def load_api_keys():
    keys = {}
    _, _, files = next(os.walk('keys'))
    file_count = len(files)
    for i in range(file_count):
        with open(f'keys/{files[i]}', 'r') as file:
            if files[i].split('.')[-1] == 'txt':
                data = ''.join(file.readlines()).strip()
                api_name = files[i].split('.')[0].split('_')[-1]
                keys[api_name] = data
    return keys

api_keys = load_api_keys()
print(api_keys)

urls = {'unsplash': f'https://api.unsplash.com/photos/?client_id={key}'}

def get_api_data(url, key):
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key={key}'
    content = ''
    # Makes a request for the data
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())  # Decode and parse JSON data into dictionary
    print(data)
    
get_api_data(urls['unplash'], api_keys['unsplash'])