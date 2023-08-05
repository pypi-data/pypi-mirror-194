from flask import request
import json
import base64
import io
from PIL import Image
import re

def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def preprocess(d):
    #print(d['file']) #iVBORw...w9RndTMZLiy1AAAAABJRU5ErkJggg==
    #print(type(d['file'])) #<class 'str'>
    d_ = {}
    for key in d:
        value = d[key]
        if value.startswith('data:') : #Image
            #print(value) #data:image/jpeg;base64,/9j/4TT...
            value = value.replace("data:", "") #data url 부분 제거
            value = re.sub('^.+,', '', value) 
            #print(value) #/9j/4TT...
            bytes = base64.b64decode(value) 
            bytesIO = io.BytesIO(bytes)
            value = Image.open(bytesIO)
        elif is_float(value):
            value = float(value)
        d_[key] = value
    return d_

def image_to_base64(image):
    bytesIO = io.BytesIO()
    try:
        image.save(bytesIO, "JPEG")
    except:
        image.save(bytesIO, "PNG")
    b64encoded = base64.b64encode(bytesIO.getvalue())
    base64_str = b64encoded.decode("utf-8")
    return base64_str

def postprocess(d):
    d_ = {}
    for key in d:
        value = d[key]
        if str(type(value)) == "<class 'PIL.PngImagePlugin.PngImageFile'>": 
            value = image_to_base64(value)
        d_[key] = value
    return d_

def rest_api(request, predict_function):
    payload = request.get_json()
    data = payload['data']
    #print(data) #[{'a': 1, 'b': 2}]
    postprocessed_examples = []
    for example in data:
        preprocessed_example = preprocess(example)
        #print(example) #{'file': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=561x561 at 0x7F8457E79A30>}
        output_example = predict_function(**preprocessed_example)
        postprocessed_example = postprocess(output_example)
        postprocessed_examples.append(postprocessed_example)
    j = json.dumps({'data': postprocessed_examples})
    return j
