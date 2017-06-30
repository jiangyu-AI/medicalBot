"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""Builds the information extracter for extract information from baike medical webpages.
Implement the inference/loss/training pattern for model building.
1. inference() - Builds the model as far as required for running the network
forward to make predictions.
2. loss() - Adds to the inference model the layers required to generate loss.
3. training() - Adds to the loss model the Ops required to generate and
apply gradients.
This file is used by the various "fully_connected_*.py" files and not meant to
be run.
"""
import glob
import os
import codecs
import json
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import OrderedDict
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

# extract information from webpages
def extractInfoFromFile(inDir, fileId):
    # open local file
    soup = BeautifulSoup(open(inDir + '/' + fileId, encoding = 'utf-8'), 'lxml')
    # open url of webpage
    #pageUrl = 'http://baike.baidu.com/item/%E9%A2%88%E6%A4%8E%E7%97%85/261033'
    #pageFile = urlopen(pageUrl)
    #pageHtml = pageFile.read()
    #pageFile.close()
    #soup = BeautifulSoup(pageHtml, 'lxml')

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
    contentBoxes = soup.find_all('div', attrs={'class':'para-title level-2'})
    for contentBox in contentBoxes:
        contentKey = contentBox.get_text().strip('/\n').strip(name)
        contentValues = []
        while contentBox.find_next_sibling('div',attrs={'class':'para'}) != None:
            contentBox = contentBox.find_next_sibling('div',attrs={'class':'para'})
            contentValues.append(contentBox.get_text().strip('/\n').strip(name))
            data[name][contentKey] = '\n'.join(contentValues)

    return data

def writeToJson(data, outDir, fileName):
    # write data to json file
    #print(fileName)
    with open((outDir + '/' + fileName).encode('utf-8'), 'w', encoding='utf-8') as outfile:
        json_text = json.dumps(data, indent=4, ensure_ascii=False)
        outfile.write(json_text)
       # json_text_splitted = json_text.split('/n')
       # for text_ele in json_text_splitted:
       #     outfile.write(text_ele + '\n')
       #for pair in data:
       #    print(pair.encode('utf-8'))
       #json.dumps(data, outfile, ensure_ascii=False).encode('utf8')
    #with open('dataBaike.json', encoding='utf8') as dataRead:
    #    print(json.load(dataRead))

if __name__ == '__main__':
    # path to baike medical pages in local folder
    inDir = '/home/wechaty/data/webpages/disease'
    outDir = '/home/wechaty/data/jsonFiles/disease'

    #testLimit = 10
    for fileId in os.listdir(inDir):
        #if testLimit < 0:
        #    break
        #testLimit = testLimit - 1
        data = extractInfoFromFile(inDir, fileId)
        fileName = list(data.keys())[0]
        writeToJson(data, outDir, fileName)

