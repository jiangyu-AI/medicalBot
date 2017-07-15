import os

dir_in = '/home/jyu/data/baike/webpages'
dir_out = '/home/jyu/data/baike/jsonFiles'

leaf_dirs = set()
for root, dirs, files in os.walk(dir_in):
    #print(root)
    
    for name in files:
        path_file = os.path.join(root, name)
        dir_leaf_html = os.path.dirname(path_file)
        dir_leaf_json = dir_leaf_html.replace(dir_in, dir_out, 1)
        leaf_dirs.add(dir_leaf_json)
    '''  
    for name in dirs:
        print(name)
    ''' 
for leaf_dir in leaf_dirs:
    print(leaf_dir)
