import easyocr
import utils
import locale


def detectimagetext(file):
    try:
        img = utils.readimagefile(file)
    except:
        return {
            "success": False,
            "error": "read image file error"
        }
    try:
        reader = easyocr.Reader(['en', 'tr'])
        result = reader.readtext(img)
    except:
        return {
            "success": False,
            "error": "easyocr error"
        }
    destructeddata = destructimagedata(result)
    return destructeddata


def destructimagedata(data):
    list = []
    try:
        locale.setlocale(locale.LC_MONETARY, "tr_TR")
    except:
        return {
            "success": False,
            "error": "locale.setlocale(locale.LC_ALL, 'tr_TR') - error"
        }

    for i in range(len(data)):
        try:
            a = locale.atof(data[i][1])
            isnumeric = isinstance(a, float)
        except:
            isnumeric = False
        item = {
            "text": data[i][1],
            "height": int(data[i][0][2][1] - data[i][0][1][1]),
            "accuracy": data[i][2],
            "isnumeric": isnumeric
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
