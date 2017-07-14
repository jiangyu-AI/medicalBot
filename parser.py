import glob
import os
import json
from collections import OrderedDict
from bs4 import BeautifulSoup

def extractInfoFromFile(inDir, fileId):
    file_path = inDir + '/' + fileId
    with open(file_path) as f:
        soup = BeautifulSoup(f, 'html5lib')
#print(soup.prettify())

    data = {}

    main_content = soup.find('div', attrs={'class':'main-content'})
# get title
    name_box = soup.find('h1')
    name = name_box.get_text().strip('\n')
    data[name] = OrderedDict()

# add url
    url = 'http://baike.baidu.com/item/' + name + '/' + fileId
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


def writeToJson(data, outDir, fileId):
    filePath = outDir + '/' + fileId
    with open(filePath, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # path to baike medical pages in local folder
    #inDirRoot = '/home/jyu/dataTest/baikeMedical/webpages'
    #outDirRoot = '/home/jyu/dataTest/baikeMedical/jsonFiles'
    inDirRoot = '/home/jyu/data/baikeThird/science'
    outDirRoot = '/home/jyu/data/baikeThird/jsonFiles'

    os.makedirs(outDirRoot, exist_ok=True)
    inDirs = [x[0] for x in os.walk(inDirRoot)]
    for inDir in inDirs[1:]:
        outDir = outDirRoot + '/' + inDir.split('/')[-1]
        os.makedirs(outDir, exist_ok=True)
        for fileId in os.listdir(inDir):
            if fileId.endswith('.txt'):
                continue
            data = extractInfoFromFile(inDir, fileId)
            writeToJson(data, outDir, fileId)

