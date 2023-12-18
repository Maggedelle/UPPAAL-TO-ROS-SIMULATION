import urllib.request
import os
import ssl
import json

import torch
import torchvision
from torchvision import transforms
from torchvision.utils import draw_bounding_boxes
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Using Pytorch to draw results
def draw_response_pytorch(image_path, response_result):
    # Draw bounding boxes
    bboxes = []
    labels = []
    response_data = json.loads(response_result)

    # Scale image properly here (as to how Grundfos model scales images)
    with Image.open(image_path) as img:
        width, height = img.size

        if width < height:
            new_width = 640
            new_height = int((height / width) * 640)
        else:
            new_width = int((width / height) * 640)
            new_height = 640
        
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

    for box_info in response_data['boxes']:
        topX = box_info['box']['topX']
        topY = box_info['box']['topY']
        bottomX = box_info['box']['bottomX']
        bottomY = box_info['box']['bottomY']
        label = box_info['label']

        # bounding box in (xmin, ymin, xmax, ymax) format
        bbox = [bottomX*new_width, bottomY*new_height, topX*new_width, topY*new_height]
        bboxes.append(bbox)
        labels.append(label)

    bboxes = torch.tensor(bboxes)
    transform = transforms.Compose([transforms.PILToTensor()])
    image = transform(resized_img)
    
    # Create final image
    image = draw_bounding_boxes(image, bboxes, width=3, colors="red", fill=True, labels=labels, font='fonts/arialbold.ttf', font_size=20)
    image = torchvision.transforms.ToPILImage()(image) 
    image.show() 

# Using Matlab to draw results
def draw_response_matplotlib(image_path, response_result):
    with Image.open(image_path) as img:
        width, height = img.size
        if width < height:
            new_width = 640
            new_height = int((height / width) * 640)
        else:
            new_width = int((width / height) * 640)
            new_height = 640
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    fig, ax = plt.subplots(1)
    ax.imshow(resized_img)

    response_data = json.loads(response_result.decode("utf-8"))

    for box_info in response_data['boxes']:
        topX, topY, bottomX, bottomY = box_info['box']['topX'], box_info['box']['topY'], box_info['box']['bottomX'], box_info['box']['bottomY']
        label = box_info['label']+": "+str(round(box_info['score'], 3))

        # Convert normalized coordinates to pixel coordinates
        box_coords = (topX * new_width, topY * new_height, bottomX * new_width, bottomY * new_height)

        # Actual bounding box
        rect = patches.Rectangle((box_coords[0], box_coords[1]), box_coords[2] - box_coords[0], box_coords[3] - box_coords[1], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(box_coords[0], box_coords[1] - 5, label, color='white', bbox=dict(facecolor='r', edgecolor='none', boxstyle='square, pad=0.0'))

    ax.axis('off')
    plt.show()

# Function to run model series inference
def run_pumpmodel():
    url = 'https://pump-detection-1.northeurope.inference.ml.azure.com/score'
    api_key = 'Iu6dwaxhG038tQ0738TRwnLoga70HSuL'
    headers = {'Content-Type':'application/> octet-stream', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'pumpdetectionpytorch-1' }

    # POST Request
    img = 'pics/all_pumps.jpg'
    data = open(img, 'rb').read()
    req_post = urllib.request.Request(url, data, headers=headers, method="POST")

    try:
        response_post = urllib.request.urlopen(req_post)
        result = response_post.read()
        print("Post request result: ", result)
        draw_response_matplotlib(img, result)

    except urllib.error.HTTPError as error:
        print("The POST request failed with status code: " + str(error.code))
        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

# Function to run model binary inference
def run_pumpdetection():
    url = 'https://pump-detection-1.northeurope.inference.ml.azure.com/score'
    api_key = 'Iu6dwaxhG038tQ0738TRwnLoga70HSuL'
    headers = {'Content-Type':'application/> octet-stream', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'pumpdetectionpytorch-1' }

    # POST Request
    img = 'pics/blueflux.jpg'
    data = open(img, 'rb').read()
    req_post = urllib.request.Request(url, data, headers=headers, method="POST")

    try:
        response_post = urllib.request.urlopen(req_post)
        result = response_post.read()
        response_data = json.loads(result.decode("utf-8"))

        if response_data['boxes'] == []: # e.g. b'{"filename": "/tmp/tmpyxfzybjt/tmptv601ser", "boxes": []}\n'
            result = False
        else:
            result = True

        print("Post request result: ", result)
    
    except urllib.error.HTTPError as error:
        print("The POST request failed with status code: " + str(error.code))
        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

run_pumpdetection()