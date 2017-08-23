#from nltk.tokenize import StanfordTokenizer
import gzip
from hanziconv import HanziConv
import glob
import os
import json

def get_names(file_path):
    # get Chinese names, English names and id from json files
    names = []
    keys_en = {'外文名称','外文名','英文名称','英文别名'}
    keys_zh = {'中文名', '又称', '别名', '别称', '中医病名','中文别名', '中文学名'}
    with open(file_path, 'r') as f:
        data = json.load(f)
    for key, value in data.items():
        title = key
        names.append(title)
        basic = value['基本信息']
        if type(basic) is not dict:
            continue
        for key_basic, value_basic in basic.items():
            if key_basic.replace(' ', '') in keys_en:
                names.extend([name_en.lower() for name_en in basic[key_basic].replace('；', '，').split('，') if len(name_en) > 0])
            if key_basic.replace(' ', '') in keys_zh:
                names.extend([HanziConv.toSimplified(name_zh) for name_zh in basic[key_basic].replace('；', '，').split('，') if len(name_zh) > 0 and not name_zh == title]) 
    return title, names

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

def write_to_file(data, out_file):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False)
        #f.write('\n'.join(list_data))
        #json_text = json.dumps(data, indent=4, ensure_ascii=False)
        #outfile.write(json_text)

if __name__ == '__main__':
    # path to baike medical pages in local folder
    IN_DIR = '/home/jyu/data/baike/jsonFiles'
    OUT_FILE = '/home/jyu/data/baike/title_names.txt'
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
                print(title_names[title] + names_cur)
                #title_names[title] = title_names[title] + name
            else:
                title_names[title] = names_cur
    print(len(title_names))
    write_to_file(title_names, OUT_FILE)

    # debug info
    print('Number of files that have English name: ' + str(count_names_en))
    print('Number of files: ' + str(count_names))
    #print('Ratio of files that have English names: ' + str(count_names_en / count_names))

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
