import io
import cv2
import numpy as np
import datetime
import math
from PIL import Image

def read_image_file(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img


def crop_image(image_file):
    image = read_image_file(image_file)
    y, x, c = image.shape
    y_start = math.ceil(y * 0.40)
    y_end = math.ceil(y * 0.65)
    cropped_image = image[y_start:y_end, :, :]
    resized_image = cv2.resize(cropped_image, (800,320),interpolation = cv2.INTER_AREA)
    # img_show=Image.fromarray(resized_image,"RGB")
    # img_show.show()
    return resized_image

def resize_image(img):
    y, x,c= img.shape
    y_start = math.ceil(y * 0.35)
    y_end = math.ceil(y * 0.65)
    cropped_image = img[y_start:y_end, :,:]
    resized_image = cv2.resize(cropped_image, (800, 320), interpolation=cv2.INTER_AREA)
    return resized_image

def prepare_elastic_data(data,geolocation):
    substring_list = ['yerli', 'üretim', 'türkiye', 'birim', 'fiyatı', 'kdv', 'dahil', 'fiyat',"tl"]
    description = ""
    price=0
    price_text=""
    text_list=data["result"]['text_list']
    num_list=data["result"]['num_list']
    for i in range(len(text_list)):
        if i<20:
            text = text_list[i]['text']
            res = any(map(text.lower().__contains__, substring_list))
            if not res:
                description += ' ' + text
    try:
        price=float(num_list[0]['text']) if len(num_list) > 0 else 0
    except:
        price_text=num_list[0]['text']
    return {
        "definition": description,
        "price":price,
        "price_text":price_text,
        "create_date": datetime.datetime.now(),
        "geolocation":geolocation
    }
