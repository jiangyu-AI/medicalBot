# July 2017
# ==============================================================================
"""
parse webpages from baidu baike science
https://baike.baidu.com/item/%E9%BA%BB%E7%96%B9/87596
"""
import glob
import os
import json
from collections import OrderedDict
from bs4 import BeautifulSoup

def extractInfoFromFile(path_html):
    with open(path_html) as f:
        soup = BeautifulSoup(f, 'html5lib')
    data = {}
    main_content = soup.find('div', attrs={'class':'main-content'})
# get title
    title_box = soup.find('h1')
    title = title_box.get_text().strip('\n')
    data[title] = OrderedDict()

# add url
    url = 'https://baike.baidu.com/item/' + title
    data[title]['url'] = url

# get summary
    try:
        summary_box = soup.find('div', attrs={'class':'lemma-summary'})
        summary = summary_box.get_text().strip('\n')
        data[title]['summary'] = summary
    except:
        data[title]['summary'] = ''

# get basics
    try:

        basic_box = soup.find('h2', attrs={'class':'headline-1 custom-title'})
        basic_dic = OrderedDict()
        basic_item_boxes = soup.find_all('dt', attrs={'class':'basicInfo-item name'})
        for basic_item_box in basic_item_boxes:
            basic_item_key = basic_item_box.get_text().strip('\n')
            basic_item_value = basic_item_box.find_next_sibling('dd').get_text().strip('\n')
            basic_dic[basic_item_key] = basic_item_value
        data[title]['basics'] = basic_dic
    except:
        data[title]['basic'] = {}

# get content
    try:
        content_key_boxes = soup.find_all('div', attrs={'class':'para-title level-2'})
        for content_key_box in content_key_boxes:
            content_key = content_key_box.get_text().strip('\n')#.replace('\n编辑', '')#.replace(title, '')
            if len(content_key) > len(title) + 1 and content_key[:len(title)] == title and content_key[len(title):len(title)+1] != '的':
                content_key = content_key[len(title):]
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
                content_value = content_value_box.get_text().strip().strip('\n')
                #if len(content_value) > len(title) + 1 and content_value[:len(title)] == title and content_value[len(title):len(title)+1] != '的':
                #    content_values.append(content_value[len(title):])
                #else:
                content_values.append(content_value)
                content_value_box = content_value_box.find_next_sibling()
            data[title][content_key] = content_values
    except:
        pass
    return data

def writeToJson(data, path_json):
    dir_out = os.path.dirname(path_json)
    os.makedirs(dir_out, exist_ok=True)
    with open(path_json, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # path to baike webpages in local folder
    DIR_IN = '/home/jyu/data/baike/webpages/'
    DIR_OUT = '/home/jyu/data/baike0725/jsonFiles/'
    os.makedirs(DIR_OUT, exist_ok=True)
    for root, dirs, files in os.walk(DIR_IN):
        for file_name in files:
            if file_name.endswith('.txt'):
                continue
            #print(file_name)
            path_html = os.path.join(root, file_name)
            try:
                data = extractInfoFromFile(path_html)
            except:
                print(path_html)
            if data:
                for key in data:
                    title = key
                #except:
                #        print('can\'t extract information from file: ' + path_html)
                path_json = os.path.join(root, title).replace(DIR_IN, DIR_OUT, 1)
                #path_json = path_html.replace(DIR_IN, DIR_OUT, 1)
                #print(path_json)
                writeToJson(data, path_json)
