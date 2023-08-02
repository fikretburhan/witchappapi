import json

import easyocr
import utils
import locale
import re
import logging

def detectimagetext(img):
    try:
        reader = easyocr.Reader(['en', 'tr'],gpu=True)
        result = reader.readtext(img)
    except Exception as error:
        return {
            "success": False,
            "error": error
        }
    #destructeddata = destructimagedata(result)
    #return destructeddata
    return result


def destructimagedata(data):
    list = []

    for i in range(len(data)):
        checkIsText = re.search('[a-zA-Z]', data[i][1])
        text = data[i][1]
        isnumeric = False
        if not checkIsText:
            isnumeric = True
            if data[i][1].__contains__(','):
                text = data[i][1].replace(',', '.')
        # try:
        #     a = locale.atof(data[i][1])
        #     isnumeric = isinstance(a, float)
        # except:
        #     isnumeric = False
        item = {
            "text": text,
            "height": int(data[i][0][2][1] - data[i][0][1][1]),
            "accuracy": data[i][2],
            "isnumeric": isnumeric,
            # "isnumeric":False
        }
        list.append(item)
    sortedlist = sorted(list, key=lambda a: a['height'], reverse=True)
    numlist = []
    textlist = []
    for i in range(len(sortedlist)):
        if sortedlist[i]['isnumeric']:
            numlist.append(sortedlist[i])
        else:
            textlist.append(sortedlist[i])

    return {
        "numlist": numlist,
        "textlist": textlist
    }


def filterlist(x):
    if x['isnumeric']:
        return True
    else:
        return False
