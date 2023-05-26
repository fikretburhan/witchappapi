import io
import cv2
import numpy as np
import datetime
import math


def readimagefile(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    return img


def crop_image(request):
    image_file = request.files['my_img']
    image = readimagefile(image_file)
    y, x, c = image.shape
    y_start = math.ceil(y * 0.35)
    y_end = math.ceil(y * 0.65)
    cropped_image = image[y_start:y_end, :, :]

    return cropped_image


def prepareelasticdata(data):
    substring_list = ['yerli', 'üretim', 'türkiye', 'birim', 'fiyatı', 'kdv', 'dahil', 'fiyat']
    description = ""
    price=0
    pricetext=""
    for i in data['textlist']:
        text = i['text']
        res = any(map(text.lower().__contains__, substring_list))
        if not res:
            description += ' ' + text
    try:
        price=float(data['numlist'][0]['text']) if len(data['numlist']) > 0 else 0
    except:
        pricetext=data['numlist'][0]['text']
    return {
        "definition": description,
        "price":price,
        "pricetext":pricetext,
        "createdate": datetime.datetime.now()
        # "createdate": datetime.datetime.now(tz=timezone("Europe/Istanbul"))
    }
