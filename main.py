from flask import request, Flask
from utils import prepareelasticdata
from ocr import objectdetection

import json
app=Flask(__name__)

@app.route('/getname')
def home():
    return "Flask google cloud app demo ci cd test3"

@app.route("/getimagetext", methods=["post"])
def getimagetext():
    file = request.files['my_img']
    ocrresult = objectdetection.detectimagetext(file)
    elkresult=prepareelasticdata(ocrresult)
    resdata = json.dumps(elkresult,indent=4, sort_keys=True, default=str,ensure_ascii=False)
    return resdata

if __name__ == '__main__':
    app.run(port=5000)

