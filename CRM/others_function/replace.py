def replacce(obj):
    obj = str(obj)
    obj = obj.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
    return obj