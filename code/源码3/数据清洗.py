import json

f = open("./energy_data.json","r",encoding="utf-8")
# print(type(f))
raw_data = json.load(f)
f.close()
print(raw_data)


def select_num(data):
    clean_data = []
    for i in data:
        for j in i:
            try:
                num=float(j)
            except (ValueError,TypeError):
                continue
            if num >= 80:
                clean_data.append(num)
    return clean_data

def normalize(data,base=100):
    normalize_data = []
    for i in data:
        nm = i/base
        normalize_data.append(nm)
    return normalize_data

clean_data=select_num(raw_data)
print(clean_data)
normalize_data=normalize(clean_data)
print(normalize_data)

def warning_data(data,threshold_value=1.0):
    warning_data = []
    for i in data:
        if i>threshold_value:
            tup=(i,"核心过载")
            warning_data.append(tup)
        else:
            tup=(i,"运转正常")
            warning_data.append(tup)
    return warning_data
warning_data=warning_data(normalize_data)
print(warning_data)

f1=open("./clear_data.json","w",encoding="utf-8")
json.dump(warning_data,f1,ensure_ascii=False,indent=4)
f1.close()
"""
f1=open("./clear_data.txt","w",encoding="utf-8")
f1.write(str(warning_data))
f1.close()
"""