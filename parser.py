import glob
import os
import json
from collections import OrderedDict
from bs4 import BeautifulSoup

def extractInfoFromFile(path_html):
    with open(path_html) as f:
        soup = BeautifulSoup(f, 'html5lib')
#print(soup.prettify())

    data = {}

    main_content = soup.find('div', attrs={'class':'main-content'})
# get title
    name_box = soup.find('h1')
    name = name_box.get_text().strip('\n')
    data[name] = OrderedDict()

# add url
    url = 'http://baike.baidu.com/item/' + name + '/' + path_html.split('/')[-1] 
    data[name]['url'] = url

# get summary
    summary_box = soup.find('div', attrs={'class':'lemma-summary'})
    summary = summary_box.get_text().strip('\n')
    data[name]['摘要'] = summary

# get basic info
    basic_box = soup.find('h2', attrs={'class':'headline-1 custom-title'})
    basic_dic = OrderedDict()
    basic_item_boxes = soup.find_all('dt', attrs={'class':'basicInfo-item name'})
    for basic_item_box in basic_item_boxes:
        basic_item_key = basic_item_box.get_text().strip('\n')
        basic_item_value = basic_item_box.find_next_sibling('dd').get_text().strip('\n')
        basic_dic[basic_item_key] = basic_item_value
    data[name]['基本信息'] = basic_dic

# get content
    content_key_boxes = soup.find_all('div', attrs={'class':'para-title level-2'})
    for content_key_box in content_key_boxes:
        content_key = content_key_box.get_text().strip('\n')#.replace(name, '')
        if content_key[:len(name)] == name:
            content_key = content_key[len(name):]
        #print(content_key)
        content_values = []
        content_value_box = content_key_box.find_next_sibling()
        while content_value_box != None:
            if not content_value_box.has_attr('class'):
                break
            if 'level-2' in content_value_box.attrs['class']:
                break
            if 'anchor-list' in content_value_box.attrs['class']:
                content_value_box = content_value_box.find_next_sibling()
                continue
            content_value = content_value_box.get_text().strip('\n')
            if content_value[:len(name)] == name:
                content_values.append(content_value[len(name):])
            else:
                content_values.append(content_value)
            content_value_box = content_value_box.find_next_sibling()
        data[name][content_key] = content_values

    return data


def writeToJson(data, path_json):
    dir_out = os.path.dirname(path_json)
    os.makedirs(dir_out, exist_ok=True)
    with open(path_json, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # path to baike webpages in local folder
    dir_in = '/home/jyu/data/baike/webpages'
    dir_out = '/home/jyu/data/baike/jsonFiles2'
    os.makedirs(dir_out, exist_ok=True)

    for root, dirs, files in os.walk(dir_in):
        for file_name in files:
            if file_name.endswith('.txt'):
                continue
            path_html = os.path.join(root, file_name)
            path_json = path_html.replace(dir_in, dir_out, 1)
            data = extractInfoFromFile(path_html)
            writeToJson(data, path_json)

