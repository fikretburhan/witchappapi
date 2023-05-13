import io
import cv2
import numpy as np
import datetime
from pytz import timezone
import locale


def readimagefile(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    return img


def prepareelasticdata(data):
    substring_list = ['yerli', 'üretim', 'türkiye', 'birim', 'fiyatı','kdv','dahil','fiyat']
    description = ""
    for i in data['textlist']:
        text = i['text']
        res = any(map(text.lower().__contains__, substring_list))
        if not res:
            description += ' ' + text
    return {
        "definition": description,
        "price": float(data['numlist'][0]['text']) if len(data['numlist']) > 0 else 0,
        #"price": locale.atof(data['numlist'][0]['text']) if len(data['numlist']) > 0 else 0,
        "createdate": datetime.datetime.now()
        #"createdate": datetime.datetime.now(tz=timezone("Europe/Istanbul"))
    }
