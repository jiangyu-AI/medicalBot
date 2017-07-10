"""
Builds the information extracter for extract information from baike medical related webpages.
Change inDir and outDir to parse different sources
July 2017
"""
import glob
import os
import codecs
import errno
import json
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import OrderedDict

def extractInfoFromFile(inDir, fileId):
    # open local file
    with open(inDir + '/' + fileId, encoding = 'utf-8') as fp:
        soup = BeautifulSoup(fp, 'lxml')

    # create a dict to store all the data being pulled from webpages
    data = OrderedDict()
    # get the title
    nameBox = soup.find('h1')
    name = nameBox.get_text().strip('/\n')
    data[name] = OrderedDict()
    # add url
    url = 'http://baike.baidu.com/item/' + name + '/' + fileId
    data[name]['url'] = url
    #print(url.encode('utf-8'))
    # get the summary
    summaryBox = soup.find('div', attrs={'class':'lemma-summary'})
    summary = summaryBox.get_text().strip('/\n')
    data[name]['摘要'] = summary
    # get basic info
    basicBox = soup.find('h2', attrs={'class':'headline-1 custom-title'})
    basic = '基本信息'
    #basic = basicBox.get_text()
    basicDict = OrderedDict()
    basicItemNameBoxes = soup.find_all('dt', attrs={'class':'basicInfo-item name'})
    for basicItemNameBox in basicItemNameBoxes:
        basicItemName = basicItemNameBox.get_text().strip('/\n')
        basicItemValue = basicItemNameBox.find_next_sibling('dd').get_text().strip('/\n')
        basicDict[basicItemName] = basicItemValue
    data[name][basic] = basicDict

    # get the contents
    content_key_boxes = soup.find_all('div', attrs={'class':'para-title level-2'})
    for content_key_box in content_key_boxes:
        #print(content_key_box.get_text())
        content_key = content_key_box.get_text().strip('/\n').replace(name, "")
        content_values = []
        content_value_box = content_key_box.find_next_sibling('div')#,attrs={'class':'para'})
        print(content_value_box.encode('utf-8').prettify(formatter='xml'))
        while content_value_box != None:
            try:
                attrs = content_value_box.div['class']
                print('sibling is ' + attrs)
            except AttributeError:
                attrs = ""
            if attrs == u'para':
                content_values.append(content_value_box.get_text())
                content_value_box = content_value_box.next_sibling#('div',attrs={'class':'para'})
            else:
                break
        data[name][content_key] = '\n'.join(content_values)
    return data

def writeToJson(data, outDir, fileId):
    #print(fileName)
    filePath = (outDir + '/' + fileId).encode('utf-8')
    with open(filePath, 'w', encoding='utf-8') as outfile:
        json_text = json.dumps(data, indent=4, ensure_ascii=False)
        outfile.write(json_text)

if __name__ == '__main__':
    # path to baike medical pages in local folder
    inDir = '/home/jyu/data/baikeMedical/webpages/test'
    outDir = '/home/jyu/data/baikeMedical/jsonFiles/test'

   # inDir = '/home/jyu/data/baikeMedical/webpages/food'
   # inDir = '/home/jyu/data/baikeMedical/webpages/psychological'
   # inDir = '/home/jyu/data/baikeMedical/webpages/bioMedical'
   # inDir = '/home/jyu/data/baikeMedical/webpages/chemical'

   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/food'
   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/psychological'
   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/bioMedical'
   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/chemical'

    os.makedirs(outDir, exist_ok=True)
    for fileId in os.listdir(inDir):
        data = extractInfoFromFile(inDir, fileId)
        #fileName = list(data.keys())[0]
        #print(fileName.encode('utf-8'))
        writeToJson(data, outDir, fileId)

