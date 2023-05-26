from flask import request, Flask
import utils
from utils import prepareelasticdata
from ocr import objectdetection
import os
import json
from es import elsearch
import asyncio

app = Flask(__name__)


@app.route('/getname')
def home():
    data = {
        "message": "Flask google cloud app demo ci cd test4"
    }
    return json.dumps(data, indent=4, sort_keys=True, default=str, ensure_ascii=False)


@app.route("/getproducts", methods=["post"])
def getproducts():
    img = utils.crop_image(request)
    ocrresult = objectdetection.detectimagetext(img)
    elkdata = prepareelasticdata(ocrresult)
    elk_obj = elsearch.ElasticsearchClient_SSLConnction()
    result = asyncio.run(elk_obj.insert_get_doc(elkdata))
    return json.dumps(result, indent=4, sort_keys=True, default=str, ensure_ascii=False)



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
