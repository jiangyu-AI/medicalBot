from pymongo import MongoClient
import os
import time
import requests
import json 

MEDICAL_ITITLE_NAMES = '/home/jyu/data/baike/medical_title_names.txt'
MEDICAL_NAME_TITLES = '/home/jyu/data/baike/medical_name_titles.txt'
BAIKE_TITLE_TRANSLATION = '/home/jyu/data/baike/baike_title_trans.txt'
def write_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def translate(query):
    #API_ENDPOINT = "https://fanyi.baidu.com/v2transapi"
    API_ENDPOINT = 'http://translate.baidu.com/v2transapi'
    data = {'from':"zh",
            'to':"en",
            'query':query,
            'transtype':"translang",
            'simple_means_flag':"3"}
    r = requests.post(url = API_ENDPOINT, data = data)
    res_raw_json = json.loads(r.text)
    res_raw_list = res_raw_json['trans_result']['data']
    result = [] 
    for res_raw in res_raw_list:
        result.append(res_raw['src'] + ' = ' + res_raw['dst'])
    return result

def translate_titles(MEDICAL_TITLE_NAMES):
    # map different names to titles of baike medical
    # format: {name : {titles}}
    medical_name_titles_dict = {}
    with open(MEDICAL_TITLE_NAMES) as f:
    #with open('/home/jyu/data/baike/title_names.txt') as f:
        title_names = json.load(f)
    titles_zh = list(title_names.keys())
    CE_DICT = '/home/jyu/data/medical_dicts/ce.dict.txt'
    with open(CE_DICT) as f:
        lines = f.readlines()
    zh_en_dict = {}
    for line in lines:
        names = line.split('=')
        zh_en_dict[names[0].strip()] = names[1].strip()
    titles_zh_en = {}
    for title_zh in titles_zh:
        if title_zh in zh_en_dict:
            titles_zh_en[title_zh] = zh_en_dict[title_zh]
    print(len(titles_zh))
    print(len(titles_zh_en))
    write_to_file(titles_zh_en, '/home/jyu/data/baike_medical_titles_lookup.txt')


client = MongoClient('mongodb://10.96.97.228:27017/')
db = client['kg']

cols = db.collection_names()
for col in cols:
    print(col)
#collection_names = ['merck', 'bigdatalab', 'umls', 'xywy', 'baidu_baike']
#    collection = db[col].find()
kg_names_en_zh = [] 
print('processing merck')
collection = db['merck'].find()
for item in collection:
    print(item)
    break
    name_zh = item['title_chi']
    try:
        name_en = item['title_en']
    except:
        name_en = ''
    kg_names_en_zh.append(name_en + '=' + name_zh)
'''
    for key in item.keys():
        print(key)
        print(item[key])
    break
'''
print('processing bigdatalab')
collection = db['bigdatalab'].find()
for item in collection:
    print(item)
    break
    try:
        name_zh = item['name'][0]
    except:
        name_zh = ''
    name_en = ''#item['title_en']
    kg_names_en_zh.append(name_en + '=' + name_zh)

print('processing xywy')
collection = db['xywy'].find()
for item in collection:
    print(item)
    break
    name_zh = item['name']
    name_en = ''#item['title_en']
    kg_names_en_zh.append(name_en + '=' + name_zh)

print('baidu_baike')
collection = db['baidu_baike'].find()
for item in collection:
    print(item)
    break
    name_zh = item['name']
    name_en = ''#item['title_en']
    kg_names_en_zh.append(name_en + '=' + name_zh)

write_to_file(kg_names_en_zh, '/home/jyu/data/kg_names_en_zh.txt')

print('umls')
names_umls = []
collection = db['umls'].find()
for item in collection:
    print(item)
    break
    name_info_list = item['name']
    names = []
    for name_info in name_info_list:
        if name_info['lang'] == 'ENG':
            names.append(name_info['name'])
    names_umls.append(names)

write_to_file(names_umls, '/home/jyu/data/names_umls.txt')
'''
num_char_per_query = 1000
chunks = [titles_zh[x:x+num_char_per_query] for x in range(0, len(titles_zh), num_char_per_query)]
#print(zh_names)
names = [] 
for chunk in chunks:
    query = '\n'.join(chunk)
    time.sleep(1) 
    res = translate(query)
    names.extend(res)
    print(res)

write_to_file(names, '/home/jyu/data/baike_title_trans.txt')
'''
