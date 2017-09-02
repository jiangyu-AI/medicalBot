# July 2017
# ==============================================================================
"""
crawls all webpages from baidu baike science

"""
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

max_page_num = str(500) # 1 for testing, 500 for crawling all pages
URL_ROOT = 'http://baike.baidu.com/science'
#https://baike.baidu.com/science
OUT_DIR_ROOT = '/home/jyu/data/baikeFive/science'
os.system('javac Crawler.java')
lemma_nums = []

def call_crawler_java(title, tag_id, out_dir_):
    out_dir = out_dir_ + '/' + title
    os.makedirs(out_dir, exist_ok=True)
    # process all sublinks with tagId
    cmd_call_java = 'java Crawler ' + tag_id.rstrip() + ' ' + out_dir + ' ' + max_page_num
    print(cmd_call_java)
    os.system(cmd_call_java)
    url_pre = 'http://baike.baidu.com/wikitag/taglist?tagId=' 
    url = url_pre + tag_id
    r = urlopen(url).read()
    soup = BeautifulSoup(r, 'html5lib')
    lemma_num = soup.find('div', class_='lemma_num').get_text()
    lemma_nums.append(title + ' ' + lemma_num)

def download_file(url, file_path):
    try: 
        response = urlopen(url)
        web_content = response.read()
        with open(file_path, 'wb') as f:
            f.write(web_content)
        print('downloading: ' + url + '\n' + 'save to: ' + os.path.dirname(file_path))
    except:
        print('can\'t download file: ' + url)

# crawl all science categories except medical
# ==============================================================================
url_cur = URL_ROOT#queue.popleft()
out_dir = OUT_DIR_ROOT#queue_dir.popleft()
with urlopen(url_cur) as conn:
    soup = BeautifulSoup(conn.read(), 'html5lib')
for tag in soup.find_all('h4'):
    url = tag.a.attrs['href']
    url_splited = url.split('tagId=')
    title = tag.get_text()
    if len(url_splited) == 2:
        tag_id = url_splited[-1]
        call_crawler_java(title, tag_id, out_dir)

# crawl all medical categories
# ==============================================================================
#url_cur = 'https://baike.baidu.com/science/medical'
out_dir = OUT_DIR_ROOT + '/medical' 
titles = ['疾病症状', '药物', '中医药', '诊疗技术'] 
tag_ids = ['75953', '75954', '75956', '75955'] 
index_title = 0
for tag_id in tag_ids:
    title = titles[index_title]
    index_title = index_title + 1
    call_crawler_java(title, tag_id, out_dir)

# download pages from urlsBfsOnelevel from each page crawled in the above two steps
# ==============================================================================
out_dir_bfs = '/home/jyu/data/baikeFive/bfs'
os.makedirs(out_dir_bfs, exist_ok=True)
URLS_BFS_FILE = '/home/jyu/data/baikeFive/urlsBfs.txt'
URLS_BFS_FILE_SET = '/home/jyu/data/baikeFive/urlsBfsSet.txt'
VISITED_FILE = "/home/jyu/data/baikeFive/visited.txt"
VISITED_FILE_SET = "/home/jyu/data/baikeFive/visitedSet.txt"

with open(VISITED_FILE) as f:
    visited_title = set(line.strip().split('/')[4] for line in f.readlines())
    with open(VISITED_FILE_SET, 'w') as f:
        f.write('\n'.join(list(visited_title)))
with open(URLS_BFS_FILE) as f:
    urls = set(line.strip() for line in f.readlines())
    with open(URLS_BFS_FILE_SET, 'w') as f:
        f.write('\n'.join(list(urls)))
for url in urls:
    if len(url.strip('\n')) > 0 and url.split('/')[4] not in visited_title:
      file_path = out_dir_bfs + '/' + url.strip('\n').split('/')[-1]
      download_file(url, file_path) 

# out put files stats
# ==============================================================================
with open(OUT_DIR_ROOT + '/' + 'lemma_nums.txt','a') as f:
    f.write(''.join(lemma_nums))

