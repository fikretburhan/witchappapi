import elasticsearch
from flask import request, Flask
from utils import prepareelasticdata
from ocr import objectdetection
import asyncio
import os
import json
from es import elsearch

app = Flask(__name__)


@app.route('/getname')
def home():
    return "Flask google cloud app demo ci cd test4"


@app.route("/getproducts", methods=["post"])
def getproducts():
    file = request.files['my_img']
    ocrresult = objectdetection.detectimagetext(file)
    elkdata = prepareelasticdata(ocrresult)
    result = search_put_product(elkdata)
    return result


def search_put_product(elk_data):
    # resdata = json.dumps(elkresult, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    insert_result = setelkdata(elk_data)
    search_result = getelkdata(elk_data['definition'])
    return {
        "search_result":search_result,
    }


def setelkdata(resdata):
    elk_obj = elsearch.ElasticsearchClient_SSLConnction()
    res = elk_obj.insert_doc(resdata)
    return res


def getelkdata(searchTerm):
    elk_obj = elsearch.ElasticsearchClient_SSLConnction()
    res = elk_obj.get_search_data(searchTerm)
    return res


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
