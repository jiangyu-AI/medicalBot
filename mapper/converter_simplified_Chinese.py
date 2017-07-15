#!/usr/bin/python2

import io
import json
import gzip
from hanziconv import HanziConv

labels_id_wiki_file = '/home/jyu/data/wiki/labels_id.txt'
labels_id_wiki_simplified = '/home/jyu/data/wiki/labels_id_simplified.txt'

names_id_baike_file = '/home/jyu/data/baikeMedical/names_id.txt'

with io.open(labels_id_wiki_file, 'r', encoding='utf-8') as f_wiki:
    labels_id = f_wiki.readlines()

#with open(names_id_baike_file, 'r') as f_baike:
#    names_id = f_baike.readlines()

labels_id_simplified = []
for labels_id_cur in labels_id:
    labels_id_splited = labels_id_cur.split('\t')
    if len(labels_id_splited) == 3:
        name_en = labels_id_splited[0]
        name_zh = labels_id_splited[1]
        id_wiki = labels_id_splited[2]
    else:
        continue
        #print labels_id_cur
    #elif len(labels_id_splited) == 2:

    name_zh_simplified = HanziConv.toSimplified(name_zh)
    labels_id_simplified.append(name_en + '\t' + name_zh_simplified + '\t' + id_wiki)

with io.open(labels_id_wiki_simplified, 'w', encoding='utf-8') as f_out:
    f_out.write('\n'.join(labels_id_simplified))
#print(name_zh)
#print(HanziConv.toSimplified(name_zh))


labels_id_wiki_file = '/home/jyu/data/wiki/labels_id.txt'
labels_id_wiki_simplified = '/home/jyu/data/wiki/labels_id_simplified.txt'
