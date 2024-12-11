from flask import Flask, request, render_template, redirect, url_for, flash, session
import os, urllib.request, json
import requests
import base64
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

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

# Converts the bytes to a link
def convert_bytes_to_image_url(file_bytes):
    # Encode the bytes into Base64
    base64_image = base64.b64encode(file_bytes).decode("utf-8")
    # Create a data URL for the image
    image_url = f"data:image/jpeg;base64,{base64_image}"
    return image_url

def get_api_data(api, params=None, image_url=None, search=None, file_bytes=None): # api --> api we want, params for unplash image, image_url for clarifai image analysis, search for pixabay videos
    # Sets the urls
    urls = {'unsplash': f'https://api.unsplash.com/photos/random?client_id={api_keys["unsplash"]}',
        'clarifai': f'https://clarifai.com/salesforce/blip/models/general-english-image-caption-blip',
        'pixabay': f'https://pixabay.com/api/videos/?key={api_keys["pixabay"]}&q={search}'}
    # Clarifai url is unneccesary since we don't actually use it but whatever
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
        # Your PAT (Personal Access Token) can be found in the Account's Security section
        PAT = api_keys['clarifai']
        # Specify the correct user_id/app_id pairings
        # Since you're making inferences outside your app's scope
        USER_ID = "salesforce"
        APP_ID = "blip"
        # Change these to whatever model and image URL you want to use
        MODEL_ID = "general-english-image-caption-blip"
        MODEL_VERSION_ID = "cdb690f13e62470ea6723642044f95e4"
        IMAGE_URL = image_url

        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (("authorization", "Key " + PAT),)
        
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        if file_bytes == None:
            post_model_outputs_response = stub.PostModelOutputs(
                service_pb2.PostModelOutputsRequest(
                    user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                    model_id=MODEL_ID,
                    version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                    inputs=[
                        resources_pb2.Input(
                            data=resources_pb2.Data(
                                image=resources_pb2.Image(
                                    url=IMAGE_URL
                                    # base64=file_bytes
                                    )
                                )
                        )
                    ],
                ),
                metadata=metadata,
            )
        else:
            post_model_outputs_response = stub.PostModelOutputs(
                service_pb2.PostModelOutputsRequest(
                    user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                    model_id=MODEL_ID,
                    version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                    inputs=[
                        resources_pb2.Input(
                            data=resources_pb2.Data(
                                image=resources_pb2.Image(
                                    # url=IMAGE_URL
                                    base64=file_bytes
                                    )
                                )
                        )
                    ],
                ),
                metadata=metadata,
            )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception(
                "Post model outputs failed, status: "
                + post_model_outputs_response.status.description
            )

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0]

        # Get the output
        return output.data.text.raw[len('a photograph of a '):]

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

def run_api_program(user_image_url=None, image_file=None, search_request=None):
    if user_image_url != None:
        image_url = user_image_url
        description = get_api_data('clarifai', image_url=image_url)
    elif image_file != None:
        file_bytes = image_file.read()
        description = get_api_data('clarifai', file_bytes=file_bytes)
        image_url = convert_bytes_to_image_url(file_bytes)
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
        description = get_api_data('clarifai', image_url=image_url)
    search_description = description.replace(' ', '+')
    videos = get_api_data('pixabay', search=search_description)
    # Returns url of the image, text caption of the image, and a list of 5 video urls that use the description as the search keywords
    return image_url, description, videos
