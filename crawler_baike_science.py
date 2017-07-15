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

'''    class UrlNode:
        def __int__(self, url, out_dir):
            self.url = url
            self.out_dir = out_dir
'''
#class Crawler(object):

    #def process_tag(self, queue, queue_dir, visited, tag):
    
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen


# crawl all science categories except medical
max_page_num = str(500) # 1 for testing

URL_ROOT = 'http://baike.baidu.com/science'
OUT_DIR_ROOT = '/home/jyu/data/baikeFourth/science'

#visited = set()
# create queue
#root = UrlNode(url_start, out_dir_start)
#queue = deque([URL_ROOT])
#queue_dir = deque([OUT_DIR_ROOT])

# crawl_bfs(queue, queue_dir, visited)

# crawl baidu baike science excluding medical categories
# while queue:
url_cur = URL_ROOT#queue.popleft()
out_dir_cur = OUT_DIR_ROOT#queue_dir.popleft()
#print(url_cur)
#print(out_dir_cur)
with urlopen(url_cur) as conn:
    soup = BeautifulSoup(conn.read(), 'html5lib')

#if url_cur not in visited:
#    visited.add(url_cur)
    #url_cur = node_cur.url
    #out_dir_cur = node_cur.out_dir
    # open url

for tag in soup.find_all('h4'):
    #os.system('javac Crawler.java')
    #print(tag.a.attrs['href'])
    #print(tag.get_text())
    url = tag.a.attrs['href']
    url_splited = url.split('tagId=')
    title = tag.get_text()
    #print(url)
    #print(title)
    out_dir = out_dir_cur + '/' + title
    os.makedirs(out_dir, exist_ok=True)

    print(url)
    if len(url_splited) == 2:
        tag_id = url_splited[-1]
        # process all sublinks with tagId
        cmd_call_java = 'java Crawler ' + tag_id.rstrip() + ' ' + out_dir + ' ' + max_page_num
        print(cmd_call_java)
        os.system(cmd_call_java)

        url_pre = 'http://baike.baidu.com/wikitag/taglist?tagId=' 
        url = url_pre + tagId
        soup = BeautifulSoup(url, 'html5lib')
        lemma_num = soup.find('div', class_='lemma_num')
        lemma_nums.add(title + ' ' + lemma_num)

with open('lemma_nums.txt','a') as f:
    f.write(''.join(lemma_nums))
    #else:
        # add subcategories i.e. without tagId into queue for further processing
        #queue.append(url)
        #queue_dir.append(out_dir)
    #print('tag_id: ' + tag_id)
    #print('out_dir: ' + out_dir)

