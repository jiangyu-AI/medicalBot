# August 2017
# ==============================================================================
"""
crawls webpages with some medical label starting from baidu baike science using BFS
decide to include '科学' into labels_medical, because some items such as the
folloing one has only '科学' as label, but it's medical item
https://baike.baidu.com/item/%E9%81%97%E4%BC%A0%E6%80%A7%E5%85%B1%E6%B5%8E%E5%A4%B1%E8%B0%83/919024

"""
import sys
import _thread
import os
import re
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib import request, parse
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from urllib.parse import unquote
import pathlib
import json

DIR_OUT = '/home/jyu/data/baike/allBaike/'
LEMMA_DICT_FILE = DIR_OUT + 'lemma_dict.txt'
DFS_START_ITEMS_FILE = DIR_OUT + 'dfs_start_items.txt'
SCIENCE_ITEMS_FILE = DIR_OUT + 'science_items.txt'
VISITED_BAIKE_ALL_FILE = DIR_OUT + 'baike_all_items.txt'
DIR_MEDICAL = '/home/jyu/data/baike/scienceAndBfsDepth3/webpages/science/medical'
#DIR_MEDICAL = DIR_OUT + '健康医疗'
URL_ROOT = 'https://baike.baidu.com/science'
URL_PRE = 'https://baike.baidu.com/item/'
lables_medical={'疗法', '中成药', '疾病症状', '检查项目', '医学', '医疗', '医药', '药物', '诊疗', '疾病', '中药', '医学术语', '病毒', '心理学', '科学'}

class HREFParser(HTMLParser):
    """
    Parser that extracts hrefs
    """
    hrefs = set()
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            dict_attrs = dict(attrs)
            if dict_attrs.get('href'):
                self.hrefs.add(dict_attrs['href'])

def get_local_links(html, domain):
    """
    Read through HTML content and returns a tuple of links
    internal to the given domain
    """
    hrefs = set()
    parser = HREFParser()
    parser.feed(html)
    for href in parser.hrefs:
        u_parse = urlparse(href)
        if href.startswith('/'):
            # purposefully using path, no query, no hash
            hrefs.add(u_parse.path)
        else:
          # only keep the local urls
          if u_parse.netloc == domain:
            hrefs.add(u_parse.path)
    return hrefs

# get science category tags' titles, ids
# ==============================================================================
def getTags_bs4(url_root):
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

def getTags_medical_bs4(url_root, titles_root):
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


# download all science category items
# ==============================================================================
def download_science(lemma_dict_file, dir_out):
    with open(lemma_dict_file) as f:
        lemma_dict = json.load(f)
    items = []
    num_items = 0
    for tag_id in lemma_dict.keys():
        items_sub = []
        lemma_list = lemma_dict[tag_id]['lemmal_list']
        tag_titles = lemma_dict[tag_id]['tag_title']
        dir_out_cur = dir_out
        for title in tag_titles:
            dir_out_cur = os.path.join(dir_out_cur, title)
        os.makedirs(dir_out_cur, exist_ok=True)
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
            download_item(item, dir_out_cur)
            items.append(item)
            #items_sub.append(item)
        #print('num_items_sub: ' + str(num_items_sub))
        #print('len of items_sub: ' + str(len(items_sub)))
    print('expected num_items in response: ' + str(num_items))
    print('len of items actually in lemma list: ' + str(len(items)))
    return set(items)


# download single item page
# ==============================================================================
def download_item(item, dir_out):
    url = URL_PRE + item
    try:
        response = urlopen(url)
    except:
        print(url)

    if response.status != 200:
        print('can\'t open url: ' + url)
    else:
        try:
            web_content = response.read()
        except httplib.IncompleteRead as e:
            web_content = e.partial
        file_path = os.path.join(dir_out, unquote(item).replace('/', '_'))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(web_content)


# get all items in science pages
# ==============================================================================
def get_science_items(lemma_dict_file):
    with open(lemma_dict_file) as f:
        lemma_dict = json.load(f)
    items = []
    num_items = 0
    for tag_id in lemma_dict.keys():
        items_sub = []
        lemma_list = lemma_dict[tag_id]['lemmal_list']
        tag_titles = lemma_dict[tag_id]['tag_title']
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
            items.append(item)
            #items_sub.append(item)
        #print('num_items_sub: ' + str(num_items_sub))
        #print('len of items_sub: ' + str(len(items_sub)))
    print('expected num_items in response: ' + str(num_items))
    print('len of items actually in lemma list: ' + str(len(items)))
    return items

# download all medical baike pages using DFS
# ==============================================================================
def check_is_medical(lables_cur, lables_medical):
    for lable in lables_cur:
        if lable in lables_medical or '心理学' in lable or '医学' in lable or '疾病' in lable or '医药' in lable or '医疗' in lable or '诊疗' in lable or '药物' in lable or '健康' in lable:
            return True
    return False

def download_dfs(item_start, out_dir, visited, lables, test_flag):
    p = re.compile('"/item/\S+[/\d+]*"')
    stack = [item_start]
    while stack:
        #print('len of stack: ' + str(len(stack)))
        item = stack.pop()
        if item not in visited:
            visited.add(item)
            # download page
            url = URL_PRE + item
            response = urlopen(url)
            if response.status != 200:
                print('can\'t open url: ' + url + response.status)
            else:
                try:
                    web_content = response.read()
                except httplib.IncompleteRead as e:
                    web_content = e.partial
                soup = BeautifulSoup(web_content, 'html5lib')
                tag_boxes = soup.find_all('span', attrs={'class':'taglist'})
                lables_cur = set()
                for tag_box in tag_boxes:
                    tag_text = tag_box.get_text().strip()
                    lables_cur.add(tag_text)
                lables |= lables_cur
                is_medical = check_is_medical(lables_cur, lables_medical)
                if is_medical:
                    file_path = os.path.join(out_dir, unquote(item).replace('/', '_'))
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    #print('downloading to file_path: ' + str(file_path))
                    with open(file_path, 'wb') as f:
                        f.write(web_content)
                    # push valid child items to stack
                    main_content = soup.find('div', attrs={'class':'main-content'})
                    item_list = p.findall(str(main_content))
                    for item_new in item_list:
                        item_new = item_new.strip().strip('"').strip('/item/').split('/')[0]
                        #print('item_new: ' + item_new)
                        if item_new not in visited:
                            stack.append(item_new)
                            visited.add(item_new)
                            #print('appending ' + item_new + ' to stack!')
        if test_flag:
            break  #keep only for testing
    return visited, lables

# get all items from four medical categories pages
# ==============================================================================
def get_dfs_start_items(dir_medical):
    items = set()
    for root, dirs, files in os.walk(dir_medical):
        for file_name in files:
            path_html = os.path.join(root, file_name)
            #print('path_html: ' + path_html)
            items |= get_items_from_html(path_html)
    return items

def get_items_from_html(file_path):
    items = set()
    p = re.compile('"/item/\S+[/\d+]*"')
    with open(file_path) as f:
        soup = BeautifulSoup(f.read(), 'html5lib')
    main_content = soup.find('div', attrs={'class':'main-content'})
    item_list = p.findall(str(main_content))
    for item in item_list:
        item = item.strip().strip('"').strip('/item/').split('/')[0]
        if item not in visited:
            items.add(item)
    return items



# download all baike items using DFS starting from science categories pages
# ==============================================================================
def download_bfs(queue, out_dir):
    p = re.compile('"/item/\S+[/\d+]*"')
    visited = set(queue)
    print('len of queue: ' + str(len(queue)))
    while queue:
        item = queue.pop()
        # download page
        url = URL_PRE + item
        #print('url: ' + str(url))
        try:
            response = urlopen(url)
        except:
            print('can\'t open url: ' + url)

        if not response or response.status != 200:
            print('can\'t open url: ' + url + response.status)
        else:
            try:
                web_content = response.read()
            except httplib.IncompleteRead as e:
                web_content = e.partial
            file_path = os.path.join(out_dir, unquote(item).replace('/', '_'))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            #print('downloading to file_path: ' + str(file_path))
            with open(file_path, 'wb') as f:
                f.write(web_content)
            soup = BeautifulSoup(web_content, 'html5lib')
            # push valid child items to queue
            main_content = soup.find('div', attrs={'class':'main-content'})
            item_list = p.findall(str(main_content))
            for item_new in item_list:
                item_new = item_new.strip().strip('"').strip('/item/').split('/')[0]
                #print('item_new: ' + item_new)
                if item_new not in visited:
                    queue.append(item_new)
                    visited.add(item_new)
                    #print('appending ' + item_new + ' to queue!')

    return visited


# main
# ==============================================================================
if __name__ == '__main__':
    # get test_flag
    try:
        input_arg = sys.argv[1]
        if input_arg == 'test':
            test_flag = True
    except:
        test_flag = False
    if test_flag:
        DIR_OUT = os.path.join(DIR_OUT, 'test')
        LEMMA_DICT_FILE = DIR_OUT + 'lemma_dict.txt'
    os.makedirs(DIR_OUT, exist_ok=True)


    # get tags list
    tag_id_titles_list = getTags(URL_ROOT)
    print('tag_id_titles_list: ' + str(tag_id_titles_list))

    # get lemma diction
    lemma_dict = {}
    for (tag_id, titles) in tag_id_titles_list:
        print("processing tag_id: " + tag_id)
        lemmaList, total = get_lemmaList(tag_id, test_flag)
        lemma_dict[tag_id]={}
        lemma_dict[tag_id]['tag_titles'] = titles
        lemma_dict[tag_id]['lemmal_list'] = lemmaList
        lemma_dict[tag_id]['total'] = total
    write_to_file(lemma_dict, LEMMA_DICT_FILE)


    # download all science category item pages
    visited = download_science(LEMMA_DICT_FILE, DIR_OUT)


    items_science = get_science_items(LEMMA_DICT_FILE)
    write_to_file(items_science, SCIENCE_ITEMS_FILE)
    print('num of science items: ' + str(len(items_science)))
    visited = set(items_science)


    # get all items in the pages of the 4 medical downloaded folders
    dfs_start_items = get_dfs_start_items(DIR_MEDICAL)
    write_to_file(list(dfs_start_items), DFS_START_ITEMS_FILE)
    with open(DFS_START_ITEMS_FILE) as f:
        dfs_start_items = set(json.load(f))

    # download all medical items starting with four medical categories using DFS
    lables = set() # only care labels in medical pages
    dir_out_webpages = os.path.join(DIR_OUT, 'dfs_webpages')
    os.makedirs(dir_out_webpages, exist_ok=True)
    for item in dfs_start_items:
        print('processing dfs starting from item: ' + item)
        visited, labels = download_dfs(item, dir_out_webpages, visited, lables, test_flag)


    # download all baidu baike items
    out_dir_webpages_baike_all = DIR_OUT
    visited_baike_items = download_bfs(items_science, out_dir_webpages_baike_all)

    # write visited, lables to files
    VISITED_FILE = os.path.join(DIR_OUT, 'visited.txt')
    LABLES_FILE = os.path.join(DIR_OUT, 'lables.txt')
    write_to_file(list(lables), LABLES_FILE)
    write_to_file(list(visited), VISITED_FILE)
    write_to_file(list(visited_baike_items), VISITED_BAIKE_ALL_FILE)
