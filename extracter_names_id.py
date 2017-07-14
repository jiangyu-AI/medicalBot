import glob
import os
import json


def extract_names_id(in_dir, file_id):
    file_path = in_dir + '/' + file_id

    has_en = False
    with open(file_path, 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            try:
                name_ch = value['基本信息']['中文名']
            except Exception as e:
                name_ch = key
            try:
                name_en = value['基本信息']['外文名']
                has_en = True
            except Exception as e:
                name_en = ' '
            names_id = name_ch + '\t' + name_en + '\t' + file_id
            return names_id, has_en


def write_to_file(list_data, out_file):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w') as f:
        f.write('\n'.join(list_data))
        #json_text = json.dumps(data, indent=4, ensure_ascii=False)
        #outfile.write(json_text)

    #with open(outDir + '/' + fileId, 'r') as json_file:
    #    data = json.load(json_file)
    #    print(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    # path to baike medical pages in local folder
    #inDirRoot = '/home/jyu/dataTest/baikeMedical/webpages'
    #outDirRoot = '/home/jyu/dataTest/baikeMedical/jsonFiles'
    #inDirRoot = '/home/jyu/data/baikeMedical/webpages'
    inDirRoot = '/home/jyu/data/baikeMedical/jsonFiles'
    #inDirRoot = '/home/jyu/data/baikeMedical/jsonFiles'
    out_file = '/home/jyu/data/baikeMedical/names_id_baike.txt'


   # inDir = '/home/jyu/data/baikeMedical/webpages/food'
   # inDir = '/home/jyu/data/baikeMedical/webpages/psychological'
   # inDir = '/home/jyu/data/baikeMedical/webpages/bioMedical'
   # inDir = '/home/jyu/data/baikeMedical/webpages/chemical'

   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/food'
   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/psychological'
   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/bioMedical'
   # outDir = '/home/jyu/data/baikeMedical/jsonFiles/chemical'


    # output list format: ["Chinese_name English_name id", "Chinese_name2 English_name2 id2"]
    names_id = []

    # extract Chinese name, English name and id from json files
    count_names_en = 0
    count_names = 0
    inDirs = [x[0] for x in os.walk(inDirRoot)]
    for in_dir in inDirs[1:]:
        for file_id in os.listdir(in_dir):
            names_id_cur, has_en = extract_names_id(in_dir, file_id)
            names_id.append(names_id_cur)
            count_names = count_names + 1
            if has_en:
                count_names_en = count_names_en + 1

    # write output to file
    write_to_file(names_id, out_file)
    print('Number of files that have English name: ' + str(count_names_en))
    print('Number of files: ' + str(count_names))
    print('Ratio of files that have English names: ' + str(count_names_en / count_names))

