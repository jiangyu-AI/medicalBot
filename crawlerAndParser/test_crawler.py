import unittest
from crawler import *

class TestCrawler(unittest.TestCase):
    TAG_ID_DISEASE = '75953'
    LEMMA_LIST_MEDICAL = []

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'Hello world'
        self.assertEqual(s.split(), ['Hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)

    def test_get_lemmaList(self):
        self.assertEqual(get_lemmaList(TAG_ID_MEDICAL), LEMMA_LIST_MEDICAL)


    for tag_id in lemma_dict.keys():
        print('processing tag_id: ' + tag_id)
        lemma_list = lemma_dict[tag_id]['lemmal_list']
        out_dir_tag = os.path.join(out_dir, tag_id)
        #dir_file = os.path.dirname(out_dir_tag)
        os.makedirs(out_dir_tag, exist_ok=True)
        # Create threads as follows
        try:
            _thread.start_new_thread(download_list, (lemma_list, out_dir_tag,))
        except:
            print("Error: unable to start thread:" + tag_id)

def download_list(lemma_list, out_dir):
    for lemma in lemma_list:
        print('downloading: ' + lemma['lemmaUrl'])
        download(lemma['lemmaUrl'], out_dir)

def download(url, out_dir):
    req = request.Request(url)
    try:
        response =  request.urlopen(req)
    except: 
        pass
    if response.status != 200:
        print(response.status)
    if len(url.split('/')) < 5:
        print('can\'t get item name from: ' + url)
        pass
    webContent = response.read()
    file_path = out_dir + url.split('/')[4]
    f = open(file_path, 'wb')
    f.write(webContent)
    f.close

def download_bfs(url_start, depth, out_dir):
    if url_start not in visited:
        queue = [url_start]
    p = re.compile('"/item/\S+[/\d+]*"')
    level = 0
    while queue:
        level = level + 1
        print('level: ' + str(level))
        urls = []
        for i in range(len(queue)):
            urls.append(queue.pop(0))
        for url in urls:
            visited.add(url)
            req = request.Request(url)
            response = request.urlopen(req)
            if response.status != 200:
                print(response.status)
            webContent = response.read()
            if len(url.split('/')) < 5:
                print('can\'t get item name from: ' + url)
                break
            file_path = out_dir + url.split('/')[4]
            dir_file = os.path.dirname(file_path)
            os.makedirs(dir_file, exist_ok=True)
            f = open(file_path, 'wb')
            f.write(webContent)
            f.close
            print('downloading: ' + url)

'''
titles = lemma_dict[tag_id]['titles']
out_dir_tag = DIR_OUT
for title in titles:
    out_dir_tag = os.path.join(out_dir_tag, title)
    os.makedirs(out_dir_tag, exist_ok=True)
'''
def backup():
    files_dir = '/home/jyu/data/baike/bfsNew'
    urls_file = '/home/jyu/data/baike/urls_bfs_new.txt'
    urls_remaining_file = '/home/jyu/data/baike/urls_remaining.txt'
    urls_downloaded = set()
    for (root, dirs, files) in os.walk(files_dir):
        for file_name in files:
            urls_downloaded.add(file_name)
    with open(urls_file) as f:
        urls_full = set(line.strip() for line in f.readlines())
    urls_remaining = urls_full - urls_downloaded
    with open(urls_remaining_file, 'w') as f:
        f.write('\n'.join(urls_remaining))

    files_dir = '/home/jyu/data/baike/bfsNew'
    urls_file = '/home/jyu/data/baike/urls_bfs_new.txt'
    urls_remaining_file = '/home/jyu/data/baike/urls_remaining.txt'
    urls_downloaded = set()
    for (root, dirs, files) in os.walk(files_dir):
        for file_name in files:
            urls_downloaded.add(file_name)
    with open(urls_file) as f:
        urls_full = set(line.strip() for line in f.readlines())
    urls_remaining = urls_full - urls_downloaded
    with open(urls_remaining_file, 'w') as f:
        f.write('\n'.join(urls_remaining))

    BAIKE_URL_PREFIX = 'https://baike.baidu.com/item/'
    baike_medical_titles_file = '/home/jyu/data/baike_medical_titles_lookup.txt'
    with open(baike_medical_titles_file) as f:
      titles_zh_en_dict = json.load(f)
    for title_zh in titles_zh_en_dict.keys():
      print(title_zh)
    print(len(titles_zh_en_dict.keys()))  

medical_tags = ['中医药', '疾病症状', '药物', '诊疗技术']
out_dir = '/home/jyu/data/baike123/'
tag_ids_titles = {'75953':'疾病症状', '75954':'药物', '75956':'中医药', '75955':'诊疗技术'}
#MEDICAL_DIR = '/home/jyu/data/baike/webpages/science/medical'
#DIR_IN = '/home/jyu/data/baike/webpages/science/medical/'


if __name__ == '__main__':
    unittest.main()
