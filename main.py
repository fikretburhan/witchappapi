from flask import request, Flask
from utils import prepareelasticdata
from ocr import objectdetection
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
    elkresult = prepareelasticdata(ocrresult)
    #resdata = json.dumps(elkresult, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    res = setelkdata(elkresult)
    return res

def setelkdata(resdata):
    elk_obj = elsearch.ElasticsearchClient_SSLConnction()
    # elk_obj.create_index()
    res = elk_obj.insert_doc(resdata)
    return res


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
