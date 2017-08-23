import json
import gzip
import glob
import os
import io
import bz2
from hanziconv import HanziConv
#from nltk.tokenize import StanfordTokenizer
#from bs4 import BeautifulSoup
# be aware that the wikidata compressed file is over 13 GB, can't be read in at once
WIKI_DIR = '/home/jyu/data/wiki/'
BAIKE_DIR = '/home/jyu/data/baike/'
WIKIDATA_FILE = WIKI_DIR + 'wikidata-20170703-all.json.gz'

ENWIKI_TITLES_NS0_FILE = WIKI_DIR + 'enwiki-20170720-all-titles-in-ns0.gz'
ENWIKI_TITLES_NS0_FILE_26 = WIKI_DIR + 'enwiki-20170726-all-titles-in-ns-0.gz'
ZHWIKI_TITLES_NS0_FILE = WIKI_DIR + 'zhwiki-20170720-all-titles-in-ns0.gz'
ENWIKI_ABSTRACT_FILE = WIKI_DIR + "enwiki-20170701-abstract.xml"
ENWIKI_PAGES_INDEX_FILE = WIKI_DIR + "enwiki-20170701-pages-articles-multistream-index.txt.bz2"
ENWIKI_PAGES_FILE = WIKI_DIR + "enwiki-20170701-pages-articles-multistream.xml.bz2"

ENWIKI_CATEGORY_SQL = WIKI_DIR + 'enwiki-20170720-category.sql.gz'
ENWIKI_LANGLINKS_SQL = WIKI_DIR + 'enwiki-20170720-langlinks.sql.gz'
ENWIKI_PAGELINKS_SQL = WIKI_DIR + 'enwiki-20170720-pagelinks.sql.gz'

ENWIKI_SEARCH_JSON = WIKI_DIR + 'enwiki-20170724-cirrussearch-content.json.gz'

EN2ZH_HTML_JSON = WIKI_DIR + 'cx-corpora.en2zh.html.json.gz'
EN2ZH_TEXT_JSON = WIKI_DIR + 'cx-corpora.en2zh.text.json.gz'
EN2ZH_TEX_TMX = WIKI_DIR + 'cx-corpora.en2zh.text.tmx.gz'

WIKIDATA_LABELS_FILE = WIKI_DIR + 'labels.txt'
CE_DICT = '/home/jyu/data/medical_dicts/ce.dict.txt'
EC_DICT = '/home/jyu/data/medical_dicts/ec.dict.txt'
BAIKE_TILE2NAMES = BAIKE_DIR + 'title_names_addTranslation.txt'

BAIKE_TITLE_NAMES_FILE = BAIKE_DIR + 'title_names.txt'
baike_names_id_file = '/home/jyu/data/baikeMedical/nameIdMapDisease.txt'#'/home/jyu/data/baikeMedical/names_id.txt'

matches_by_nameCh_file = '/home/jyu/data/disease_matches_by_nameCh.txt'
baike_title_names_addTranslation = '/home/jyu/data/baike/title_names_addTranslation.txt'

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

# get titles from wiki
def get_titles(file_path):
    titles = set()
    with gzip.open(file_path, 'rb') as f:
        for line in f:
            title = line.decode('utf-8').rstrip('\n')
            for c in title:
                if u'\u4e00' <= c <= u'\u9fff':
                    titles.add(HanziConv.toSimplified(title))
                    break
            titles.add(title)
    return titles

# get word counts from baike json file
def get_words_counts(file_path):
    with open(file_path) as f:
        data = json.load(f)
    for key, value in data.items():
        abstract = value['摘要']
        words = StanfordTokenizer().tokenize(abstract)
    words_counts_dic = {}
    for word in words:
        words_counts_dic[word] = words_counts_dic.get(word, 0) + 1
    return words_counts_dic 

def write_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

# get names from baike json file
# get Chinese names, English names and id from json files
def get_names(file_path):
    names = set()
    keys_en = {'外文名称','外文名','英文名称','英文别名'}
    keys_zh = {'中文名', '又称', '别名', '别称', '中医病名','中文别名', '中文学名'}
    with open(file_path, 'r') as f:
        data = json.load(f)
    for key, value in data.items():
        title = key
        names.add(title)
        basic = value['基本信息']
        if type(basic) is not dict:
            continue
        for key_basic, value_basic in basic.items():
            if key_basic.replace(' ', '') in keys_en:
                 name_en_list = [name_en for name_en in basic[key_basic].replace('；', '，').split('，') if len(name_en) > 0]
                 for name_en in name_en_list:
                     names.add(name_en.lower())
            if key_basic.replace(' ', '') in keys_zh:
                name_zh_list = [name_zh for name_zh in basic[key_basic].replace('；', '，').split('，') if len(name_zh) > 0 and not name_zh == title ]
                for name_zh in name_zh_list:
                    names.add(HanziConv.toSimplified(name_zh)) 
    return title, names

def get_title_names(in_dir, out_file):
    # path to baike medical pages in local folder
    # output list format: ["Chinese_name English_name id", "Chinese_name2 English_name2 id2"]
    title_names = {} 
    file_words_counts_dic = {}
    count_names_en = 0
    count_names = 0
    for root, dirs, files in os.walk(IN_DIR):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            title, names_cur = get_names(file_path)
            if title in title_names:
                print(title_names[title] + list(names_cur))
                #title_names[title] = title_names[title] + name
            else:
                title_names[title] = list(names_cur)
    return title_names

def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])
    return lcs_set

def get_exact_matches(wiki_labels_id, baike_names_id):
    labelEn_id_dic = {}
    labelCh_id_dic = {}
    for labels_id in wiki_labels_id:
        labels_id_splited = labels_id.split('\t')
        if(len(labels_id_splited) != 3):
            print(labels_id)
            continue
        labelEnRaw, labelChRaw, wiki_id = labels_id_splited
        labelEn = labelEnRaw.lower()
        labelCh = labelChRaw.lower()
        if labelEn.strip() != '':
            labelEn_id_dic[labelEn] = wiki_id
        if labelCh.strip() != '':
            labelCh_id_dic[labelCh] = wiki_id
    matches_by_nameEn = []
    matches_by_nameCh = []
    # match by simplified Chinese names
    for names_id in baike_names_id:
        try:
            nameCh, baike_id = names_id.split()
        except:
            print(names_id)
        if nameCh in labelCh_id_dic:
            wiki_id = labelCh_id_dic[nameCh]
            matches_by_nameCh.append(baike_id.strip('\n') + '\t' + wiki_id.strip('\n') + '\t' + nameCh)
    # match by lower case English names
    for labels_id in wiki_labels_id:
        try:
            nameCh, baike_id = names_id.split()
        except:
            print(names_id)
        nameEn = nameEnRaw.lower()
        if nameCh in labelCh_id_dic:
            wiki_id = labelCh_id_dic[nameCh]
            matches_by_nameCh.append(baike_id.strip('\n') + '\t' + wiki_id.strip('\n') + '\t' + nameCh)
    return matches_by_nameCh

def get_matches_by_name(wiki_titles_set, baike_title_names_dict):
    matches = {}
    for title, names in baike_title_names_dict.items():
        for name in names:
            if name in wiki_titles_set:
                matches[title] = name
                continue
    return matches

def get_matches_by_lcs(wiki_titles_set, baike_title_names_dict):
    matches = {}
    for title, names in baike_title_names_dict.items():
        for name in names:
            if name in wiki_titles_set:
                matches[title] = name
                continue
    lcs()
    
def add_translation_name(baike_title_names_file, wikidata_labels_file, baike_title_names_addTranslation):
    # read in en-zh dictionary
    with open(wikidata_labels_file) as f:
        labels_list = json.load(f)
    zh_en_dict = {}
    for label in labels_list:
        labels = label.strip().split('<->')
        label_en = labels[0]
        label_zh = labels[1]
        zh_en_dict[label_zh] = label_en
    with open(baike_title_names_file) as f:
        title_names_dict = json.load(f)
    print(len(title_names_dict))
    baike_title_names_dict = {}
    for title, names_set in title_names_dict.items():
        names = set(names_set)
        for name in names_set:
            if name in zh_en_dict:
                names.add(zh_en_dict[name])
        baike_title_names_dict[title] = list(names)
    print(len(title_names_dict))
    write_to_file(baike_title_names_dict, baike_title_names_addTranslation)

'''
    #labels = get_labels(WIKIDATA_FILE)
    #write_to_file(labels, WIKIDATA_LABELS_FILE)    

'''
'''            words_counts_dic = get_words_counts(file_path)
            for key, value in words_counts_dic.items():
                print(key + ':' + str(value))
            file_words_counts_dic[file_name] = words_counts_dic

            count_names = count_names + 1
            if has_en:
                count_names_en = count_names_en + 1
            break
'''
# write_to_file(file_words_counts_dic, os.path.join(OUT_DIR, 'words_counts.txt'))

'''
    with open(baike_names_id_file) as baike_file:
        baike_names_id = baike_file.readlines()
        
    matches_by_nameCh = get_exact_matches(wiki_labels_id, baike_names_id)

    with open(matches_by_nameCh_file, 'w') as f:
        f.write('\n'.join(matches_by_nameCh))

    with open(matches_by_nameEn_file, 'w') as f:
        f.write('\n'.join(matches_by_nameEn))
'''
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
if __name__ == '__main__':
    IN_DIR = '/home/jyu/data/baike/jsonFiles/science/medical'
    OUT_FILE = '/home/jyu/data/baike/medical_title_names.txt'
    title_names = get_title_names(IN_DIR, OUT_FILE)
    print(len(title_names))
    write_to_file(title_names, OUT_FILE)
'''    
    with gzip.open(ENWIKI_SEARCH_JSON) as f:
        for i in range(4):
            line = f.readline()
            data = json.loads(line.decode('utf-8'))
        print(json.dumps(data, indent = 4, ensure_ascii=False))
'''
'''
    wiki_titles_set = get_titles(ENWIKI_TITLES_NS0_FILE)
    matches_by_names = get_matches_by_name(wiki_titles_set, baike_title_names_dict)
    print(len(matches_by_names))
    write_to_file(matches_by_names, '/home/jyu/data/matches_by_names.txt')
'''
