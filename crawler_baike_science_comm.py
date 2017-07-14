# July 2017
# ==============================================================================

"""crawls webpages from baidu baike science

Implements the inference/loss/training pattern for model building.

1. inference() - Builds the model as far as required for running the network
forward to make predictions.
2. loss() - Adds to the inference model the layers required to generate loss.
3. training() - Adds to the loss model the Ops required to generate and
apply gradients.

This file is used by the various "fully_connected_*.py" files and not meant to
be run.

"""

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import deque

#os.system('javac Crawler.java')
max_page_num = str(500) # 1 for testing, 500 for crawling all pages

out_dir_cur = '/home/jyu/data/baikeMedical/science/communicationsTech'
titles = ['通信科技']
tag_ids = ['68041']
#with urlopen(url_cur) as conn:
#    soup = BeautifulSoup(conn.read(), 'html5lib')
index_title = 0
#for tag in soup.find_all('a', class_='more'):
lemma_nums = []
for tag_id in tag_ids:
    #title = tag.get_text()
    title = titles[index_title]
    index_title = index_title + 1

    #print('tag.span type:' + str(type(tag.span)))
    out_dir = out_dir_cur + '/' + title
    #url = tag.attrs['href']
    #print(title)
    #print(url)
    #url_splited = url.split('tagId=')
    #if len(url_splited) == 2:
        #tag_id = url_splited[-1]
    os.makedirs(out_dir, exist_ok=True)
    cmd_call_java = 'java Crawler ' + tag_id + ' ' + out_dir + ' ' + max_page_num
    print(cmd_call_java)
    #os.system(cmd_call_java)

    url_pre = 'http://baike.baidu.com/wikitag/taglist?tagId=' 
    url = url_pre + tag_id
    soup = BeautifulSoup(url, 'html5lib')
    lemma_num = soup.find('div', class_='lemma_num')
    lemma_nums.add(title + ' ' + lemma_num)

with open('lemma_nums.txt','w') as f:
    f.write(''.join(lemma_nums))

