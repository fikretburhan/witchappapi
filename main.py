from flask import request, Flask
import utils
from utils import prepare_elastic_data
from ocr import objectdetection
import json
import os
from es import elsearch
#import asyncio
from decimal import Decimal
import logging
import cv2
app = Flask(__name__)
import numpy as np

@app.route('/getname')
def home():
    data = {
        "message": "Flask ubuntu app packages updated"
    }
    return json.dumps(data, indent=4, sort_keys=True, default=str, ensure_ascii=False)

@app.route("/getproducts", methods=["post"])
def getproducts():
    image_file=request.files['my_img']
    # geolocation={
    #     "longitude":Decimal(request.form["longitude"]),
    #     "latitude":Decimal(request.form["latitude"]),
    # }
    img = utils.crop_image(image_file)
    ocr_result = objectdetection.detect_image_text(img)
    elk_data = prepare_elastic_data(ocr_result,[])
    #elk_obj = elsearch.ElasticsearchClient_SSLConnction()
    #result = asyncio.run(elk_obj.insert_get_doc(elkdata))
    #result = elk_obj.insert_get_doc(elkdata)

    return json.dumps(elk_data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
