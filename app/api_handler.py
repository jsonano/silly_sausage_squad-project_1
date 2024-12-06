from flask import Flask, request, render_template, redirect, url_for, flash, session
import os, urllib.request, json
from clarifai.client.model import Model

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

# Get API data
def get_api_data(api, params=None, image_url=None, search=None): # api --> api we want, params for unplash image, image_url for clarifai image analysis, search for pixabay videos
    # Sets the urls
    urls = {'unsplash': f'https://api.unsplash.com/photos/random?client_id={api_keys["unsplash"]}', 
        'clarifai': f'https://clarifai.com/salesforce/blip/models/general-english-image-caption-blip',
        'pixabay': f'https://pixabay.com/api/videos/?key={api_keys["pixabay"]}&q={search}'}
    url = urls[api]
    # Different processes for each api
    # Unsplash (get img)
    if api == 'unsplash':
        if params==None:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())  # Decode and parse JSON data into dictionary
            return data['urls']['full']
        else:
            img_links = []
            url = "https://api.unsplash.com/search/photos"
            # Headers
            headers = {
                "Authorization": f"Client-ID {api_keys['unsplash']}"
            }

            # Send request
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            for result in data['results']:
                img_links.append(result['urls']['regular'])
            return img_links  
    # Clarifai (img to txt)
    elif api == 'clarifai':
        # Model code from clarifai api documentation
        model_url = (url)

        model_prediction = Model(url=model_url, pat=api_keys['clarifai']).predict_by_url(image_url, input_type="image")

        # Get the output
        return model_prediction.outputs[0].data.text.raw[len('a photograph of a '):]
    # Pixabay (videos)
    else:
        video_links = []
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())  # Decode and parse JSON data into dictionary
        hits = data['hits']
        for vid in hits:
            video_links.append(vid['videos']['large']['url'])
        if data['totalHits'] < 5:
            return video_links
        else:
            return video_links[:5]

# Run the program using APIs
def run_api_program(user_image_url=None, image_file=None, search_request=None):
    # Gets the image
    if user_image_url != None:
        image_url = user_image_url
    elif image_file != None:
        return
    elif search_request != None:
        # Search parameters
        params = {
            "query": search_request,
            "page": 1,
            "per_page": 5
        }
        return get_api_data('unsplash', params=params)
    else:
        image_url = get_api_data('unsplash')
    # Gets description
    description = get_api_data('clarifai', image_url)
    # Changes description to search phrase
    search_description = description.replace(' ', '+')
    # Gets the videos
    videos = get_api_data('pixabay', search=search_description)
    return image_url, description, videos

unsplash, clarifai, pixabay = run_api_program