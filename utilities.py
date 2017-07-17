URLS_BFS_FILE = '/home/jyu/data/baike/urls_bfs_new.txt' 
URLS_BFS_DOWNLOADED_FILE = '/home/jyu/data/baike/urls_bfs_downloaded.txt' 
URLS_BFS_REMAINING_FILE = '/home/jyu/data/baike/urls_bfs_remaining.txt'

with open(URLS_BFS_FILE) as f:
    urls_bfs = set(line.strip() for line in f.readlines())

with open(URLS_BFS_DOWNLOADED_FILE) as f:
    urls_bfs_downloaded = set(line.strip() for line in f.readlines())

urls_remaining = urls_bfs - urls_bfs_downloaded

for url in list(urls_remaining):
    print(url)

with open(URLS_BFS_REMAINING_FILE, 'w') as f:
    f.write('\n'.join(list(urls_remaining)))
