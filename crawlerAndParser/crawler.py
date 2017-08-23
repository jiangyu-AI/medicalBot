# August 2017
# ==============================================================================
"""
crawls webpages with some medical label starting from baidu baike science using BFS

"""
import sys
import _thread
import os
import re
from bs4 import BeautifulSoup
from urllib import request, parse
from urllib.request import urlopen, Request
from urllib.parse import unquote
import pathlib
import json

DIR_OUT = '/home/jyu/data/baike/scienceAndMedicalBfs/'
LEMMA_DICT_FILE = '/home/jyu/data/baike/lemma_dict.txt'
URL_ROOT = 'https://baike.baidu.com/science'
URL_PRE = 'https://baike.baidu.com/item/'
lables_medical={'医学', '医疗', '医药', '药物', '诊疗', '疾病', '中药', '医学术语', '病毒'} 
DEPTH_BFS = 10000 # set it to be big to crawl all medical baike pages


# get science category tags' titles, ids
# ==============================================================================
def getTags(url_root):
    with urlopen(url_root) as conn:
        soup = BeautifulSoup(conn.read(), 'html5lib')
    tags = []
    for tag in soup.find_all('h4'):
        url = tag.a.attrs['href']
        url_splited = url.split('tagId=')
        titles = []
        titles.append(tag.get_text())
        if len(url_splited) == 2:
            tag_id = url_splited[-1]
            tags.append((tag_id, titles))
        else:
            tags.extend(getTags_medical(url, titles))
    return tags

def getTags_medical(url_root, titles_root):
    with urlopen(url_root) as conn:
        soup = BeautifulSoup(conn.read(), 'html5lib')
    tags = []
    tag_box = soup.find('ul', attrs={'class':'knowledge-list cmn-clearfix'}).find('li')
    while tag_box != None: 
        titles = list(titles_root)
        titles.append(tag_box.span.get_text())
        url = tag_box.a.attrs['href']
        url_splitted = url.split('tagId=')
        if len(url_splitted) == 2:
            tag_id = url_splitted[-1]
            tags.append((tag_id, titles))
        tag_box = tag_box.find_next_sibling()
    return tags


# get lemma list for science category tags
# ==============================================================================
def get_lemmaList(tagId, test_flag):
    url = 'https://baike.baidu.com/wikitag/api/getlemmas'
    if test_flag:
        totalPage = 0#1000 #1 for testing
        limit = '1'#'24' #1 for testing, 24
    else:
        totalPage = 1000
        limit = '24'
    page_id = 0
    lemmaList = []
    while page_id <= totalPage:
        #print("page_id: " + str(page_id) + ' of total ' + str(totalPage))
        data = {'limit':limit, 'timeout':'3000','filterTags':'%5B%5D','tagId':tagId,'fromLemma':'false','contentLength':'40','page':page_id}
        data = parse.urlencode(data).encode()
        req = Request(url, data = data)
        resp = urlopen(req)
        if resp.status != 200:
            print(tagId, page_id, resp.status, resp.reason)
            continue
        resp_json = json.loads(resp.read())
        lemmaList.extend(resp_json['lemmaList'])
        if test_flag:
            pass
        else:
            totalPage = resp_json['totalPage']  #comment this line for testing
        page_id = page_id + 1
    total = resp_json['total']
    #print('total: ' + str(total))
    #print('len of lammaList: ' + str(len(lemmaList)))
    return lemmaList, total


# write json data to file
# ==============================================================================
def write_to_file(data, file_path):
    directory = os.path.dirname(file_path)
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


# download pages using BFS with depth
# ==============================================================================
def download_bfs(queue, depth, out_dir):
    p = re.compile('"/item/\S+[/\d+]*"')
    level = 0
    lables = set()
    visited = set(queue) 
    while queue: 
        level += 1
        queue_cur = list(queue)
        queue = []
        for item in queue_cur:
           # download page
           url = URL_PRE + item
           response = urlopen(url)
           if response.status != 200:
               print(response.status)
           web_content = response.read()
           file_path = os.path.join(out_dir, unquote(item))
           #print('file_path: ' + str(file_path))
           f = open(file_path, 'wb')
           f.write(web_content)
           f.close
           print('level: ' + str(level) + '\n' + 'depth: ' + str(depth))
           # add valid child note to queue
           if level <= depth:
                soup = BeautifulSoup(web_content, 'html5lib')
                main_content = soup.find('div', attrs={'class':'main-content'})
                item_list = p.findall(str(main_content))
                for item in item_list:
                    item = item.strip().strip('"').strip('/item/')
                    url_new = URL_PRE + item
                    #print('url_new: ' + url_new)
                    tag_boxes = BeautifulSoup(urlopen(Request(url_new)).read(), 'html5lib').find_all('span', attrs={'class':'taglist'})
                    for tag_box in tag_boxes:
                        tag_text = tag_box.get_text().strip()
                        lables.add(tag_text)
                        if tag_text in lables_medical or '医学' in tag_text or '疾病' in tag_text or '医药' in tag_text or '医疗' in tag_text or '诊疗' in tag_text or '药物' in tag_text or '健康' in tag_text:
                            if url_new not in visited:
                                queue.append(item)
                                visited.add(item)
                                print(tag_text + ' is in lables_medical and appending ' + url_new + ' to queue!')
    return visited, lables


if __name__ == '__main__':
    
    try:
        input_arg = sys.argv[1]    
        if input_arg == 'test':
            test_flag = True
    except:
        test_flag = False
        #print('Please add test flag, True or False!')

    if test_flag:
        DIR_OUT = os.path.join(DIR_OUT, 'test')
        DEPTH_BFS = 1
    os.makedirs(DIR_OUT, exist_ok=True) 
    
    # get tags list
    tag_id_titles_list = getTags(URL_ROOT)
    print('tag_id_titles_list: ' + str(tag_id_titles_list))   

    # get lemma diction
    lemma_dict = {}
    for (tag_id, title) in tag_id_titles_list:
        print("processing tag_id: " + tag_id)
        lemmaList, total = get_lemmaList(tag_id, test_flag) 
        lemma_dict[tag_id]={}
        lemma_dict[tag_id]['tag_title'] = title
        lemma_dict[tag_id]['lemmal_list'] = lemmaList 
        lemma_dict[tag_id]['total'] = total
    write_to_file(lemma_dict, LEMMA_DICT_FILE)
    
    # download pages from lemma diction
    with open(LEMMA_DICT_FILE) as f:
        lemma_dict = json.load(f)
    queue = []
    num_items = 0
    for tag_id in lemma_dict.keys():
        queue_sub = []
        lemma_list = lemma_dict[tag_id]['lemmal_list']
        num_items += lemma_dict[tag_id]['total']
        num_items_sub = lemma_dict[tag_id]['total']
        for lemma in lemma_list:
            url = lemma['lemmaUrl']
            #print('lemma: ' + str(lemma))
            #print('url: ' + url)
            try:
                url_split = url.split('/')
                if len(url_split) >= 5:
                    item = url_split[4]
                else:
                    print('main: can\'t get item name from url: ' + url)
            except:
                item = lemma['lemmaTitle']
                print('get item name from lemmaTitle instead!: ' + item)
            queue.append(item)
            #queue_sub.append(item)
        #print('num_items_sub: ' + str(num_items_sub))
        #print('len of queue_sub: ' + str(len(queue_sub)))
    print('num_items: ' + str(num_items))
    print('len of queue: ' + str(len(queue)))
    dir_out_webpages = os.path.join(DIR_OUT, 'webpages')
    os.makedirs(dir_out_webpages, exist_ok=True)
    visited, lables = download_bfs(queue, DEPTH_BFS, dir_out_webpages)

    VISITED_FILE = os.path.join(DIR_OUT, 'visited.txt')
    LABLES_FILE = os.path.join(DIR_OUT, 'lables.txt')
    write_to_file(list(lables), LABLES_FILE)
    write_to_file(list(visited), VISITED_FILE)
