# July 2017
# ==============================================================================

"""
crawls webpages from baidu baike science

"""
    
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

max_page_num = str(500) # 1 for testing, 500 for crawling all pages
URL_ROOT = 'http://baike.baidu.com/science'
OUT_DIR_ROOT = '/home/jyu/data/baikeFourth/science'

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
    soup = BeautifulSoup(url, 'html5lib')
    lemma_num = soup.find('div', class_='lemma_num')
    lemma_nums.add(title + ' ' + lemma_num)

# crawl all science categories except medical
# ==============================================================================

url_cur = URL_ROOT#queue.popleft()
out_dir_cur = OUT_DIR_ROOT#queue_dir.popleft()

with urlopen(url_cur) as conn:
    soup = BeautifulSoup(conn.read(), 'html5lib')

for tag in soup.find_all('h4'):
    url = tag.a.attrs['href']
    url_splited = url.split('tagId=')
    title = tag.get_text()
    if len(url_splited) == 2:
        tag_id = url_splited[-1]
        call_crawler_java(title, tag_id, out_dir_cur)


# crawl all medical categories
# ==============================================================================
#url_cur = 'https://baike.baidu.com/science/medical'
out_dir_cur = '/home/jyu/data/baikeFourth/science/medical'
titles = ['疾病症状', '药物', '中医药', '诊疗技术']
tag_ids = ['75953', '75954', '75956', '75955']
index_title = 0
for tag_id in tag_ids:
    title = titles[index_title]
    index_title = index_title + 1


# out put files stats
# ==============================================================================
with open(OUT_DIR_ROOT + 'lemma_nums.txt','a') as f:
    f.write(''.join(lemma_nums))

