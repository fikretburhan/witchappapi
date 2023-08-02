from flask import request, Flask
import utils
from utils import prepareelasticdata
from ocr import objectdetection
import os
import json
from es import elsearch
#import asyncio
from decimal import Decimal

app = Flask(__name__)


@app.route('/getname')
def home():
    data = {
        "message": "Flask ubuntu app ocrresult test"
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
    ocrresult = objectdetection.detectimagetext(img)
    #elkdata = prepareelasticdata(ocrresult,[])
    #elk_obj = elsearch.ElasticsearchClient_SSLConnction()
    #result = asyncio.run(elk_obj.insert_get_doc(elkdata))
    #result = elk_obj.insert_get_doc(elkdata)
    ocr_check=""
    if ocrresult:
        ocr_check="ocr çalıştı"
    return json.dumps(ocr_check, indent=4, sort_keys=True, default=str, ensure_ascii=False)



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
