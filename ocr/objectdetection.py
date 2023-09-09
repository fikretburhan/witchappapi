import easyocr
import re

def detect_image_text(img):
    try:
        reader = easyocr.Reader(['en', 'tr'], gpu=True)
        result = reader.readtext(img)
    except Exception as error:
        return {
            "success": False,
            "error": error
        }
    destructed_data = destruct_image_data(result)
    return {
        "success": True,
        "result": destructed_data
    }
def destruct_image_data(data):
    list = []

    for i in range(len(data)):
        check_Is_Text = re.search('[a-zA-Z]', data[i][1])
        text = data[i][1]
        is_numeric = False
        if not check_Is_Text:
            is_numeric = True
            if data[i][1].__contains__(','):
                text = data[i][1].replace(',', '.')
        item = {
            "text": text,
            "height": int(data[i][0][2][1] - data[i][0][1][1]),
            "accuracy": data[i][2],
            "is_numeric": is_numeric,
        }
        list.append(item)
    sorted_list = sorted(list, key=lambda a: a['height'], reverse=True)
    num_list = []
    text_list = []
    for i in range(len(sorted_list)):
        if sorted_list[i]['is_numeric']:
            num_list.append(sorted_list[i])
        else:
            text_list.append(sorted_list[i])

    return {
        "num_list": num_list,
        "text_list": text_list
    }

