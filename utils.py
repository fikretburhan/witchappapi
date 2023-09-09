import io
import cv2
import numpy as np
import datetime
import math


def read_image_file(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    return img


def crop_image(image_file):
    image = read_image_file(image_file)
    np.resize(image,(200,200))
    y, x, c = image.shape
    y_start = math.ceil(y * 0.35)
    y_end = math.ceil(y * 0.65)
    cropped_image = image[y_start:y_end, :, :]
    return cropped_image


def prepare_elastic_data(data,geolocation):
    substring_list = ['yerli', 'üretim', 'türkiye', 'birim', 'fiyatı', 'kdv', 'dahil', 'fiyat']
    description = ""
    price=0
    price_text=""
    for i in data['text_list']:
        text = i['text']
        res = any(map(text.lower().__contains__, substring_list))
        if not res:
            description += ' ' + text
    try:
        price=float(data['num_list'][0]['text']) if len(data['num_list']) > 0 else 0
    except:
        price_text=data['num_list'][0]['text']
    return {
        "definition": description,
        "price":price,
        "price_text":price_text,
        "create_date": datetime.datetime.now(),
        "geolocation":geolocation
    }
