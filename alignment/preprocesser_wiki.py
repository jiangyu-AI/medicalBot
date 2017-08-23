#!/usr/bin/python2
import os
import io
import json
import gzip
from hanziconv import HanziConv
import bz2
#from bs4 import BeautifulSoup
'''
with bz2.BZ2File(INDEX_FILE) as index_f:
    index_list = index_f.readlines()
    print(line_list[0])

with bz2.BZ2File(DATA_FILE) as data_f:
    offset_pre = 0
    for index in index_list:
        offset, page_id, title = index_list.split(':')
        data = data_f.read(offset - offset_pre)
        offset_pre = offset
        soup = BeautifulSoup(data)
        print(soup.prettify()[0:1000])
        break
'''
# be aware that the wikidata compressed file is over 13 GB, can't be read in at once
WIKI_DIR = '/home/jyu/data/wiki/'
WIKIDATA_FILE = WIKI_DIR + 'wikidata-20170703-all.json.gz'
ENWIKI_TITLES_NS0_FILE = WIKI_DIR + 'enwiki-20170720-all-titles-in-ns0.gz'
ENWIKI_TITLES_FILE = WIKI_DIR + 'enwiki-20170720-all-titles.gz'
ENWIKI_ABSTRACT_FILE = WIKI_DIR + "enwiki-20170701-abstract.xml"
ENWIKI_PAGES_INDEX_FILE = WIKI_DIR + "enwiki-20170701-pages-articles-multistream-index.txt.bz2"
ENWIKI_PAGES_FILE = WIKI_DIR + "enwiki-20170701-pages-articles-multistream.xml.bz2"
ZHWIKI_TITLES_NS0_FILE = WIKI_DIR + 'zhwiki-20170720-all-titles-in-ns0.gz'

LABELS_FILE = '/home/jyu/data/wiki/labels.txt'
LABELS_SIMPLIFIED_FILE = 'home/jyu/data/wiki/labels_simplified.txt'
# ??
names_id_baike_file = '/home/jyu/data/baikeMedical/names_id.txt'

# get English label, Chinese label from wikidata
def get_labels(file_path):
    labels = []
    with gzip.open(file_path, 'rb') as f:
        for line in f:
            json_bytes = line
            json_str = json_bytes.decode('utf-8')
            if json_str[:1] != '{':
                continue
            if json_str[-2] == ',':
                data = json.loads(json_str[:-2])
            else:
                data = json.loads(json_str)
            entity_id = data['id']
            try:
                label_en = data['labels']['en']['value']
            except Exception as e:
                label_en = ''
            try:
                label_zh = data['labels']['zh']['value']
            except Exception as e:
                label_zh = ''
            if len(label_en) > 0 and len(label_zh) > 0:
                label_zh_sim = HanziConv.toSimplified(label_zh)
                labels.append(str(label_en) + '<->' + str(label_zh_sim))
    print(len(labels))
    return labels

def get_titles(file_path):
    titles = set()
    with gzip.open(file_path, 'rb') as f:
        for line in f:
            title = line.decode('utf-8').rstrip('\n')
            #title = str(line)#.strip('b').strip().strip('\'').strip('\n')
            #title = str(line).lstrip('b\'').rstrip('\'').rstrip('\n').replace('_', ' ')
            #title = str(line)#.replace(b'b\'', b'').replace(b'\n\'', b'')
            titles.add(title)
    return titles

def write_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

if __name__ == '__main__':
    #labels = get_labels(WIKIDATA_FILE)
    #write_to_file(labels, LABELS_FILE)    
    
    titles = get_titles(ENWIKI_TITLES_NS0_FILE)

    titles_iter = iter(titles)
    for i in range(10):
        print(next(titles_iter))
    print(len(titles))

