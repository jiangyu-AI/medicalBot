import os
import json
import gzip


# be aware that the wikidata compressed file is over 13 GB, can't be read in at once
wiki_13g_path = '/home/jyu/data/wiki/wikidata-20170703-all.json.gz'

labels_id = []

#
count_label_zh = 0
count_label_en = 0
count_label = 0

#labels_id_missing_en = []
with gzip.open(wiki_13g_path, 'rb') as fin:
    #count = 10000
    for line in fin:
        '''
        count = count - 1
        if count < 0:
            break
'''
        #json_bytes = fin.readline()
        json_bytes = line
        json_str = json_bytes.decode('utf-8')
        if json_str[:1] != '{':
            continue
        if json_str[-2] == ',':
            data = json.loads(json_str[:-2])
        else:
            data = json.loads(json_str)

        entity_id = data['id']
        try:
            entity_label_en = data['labels']['en']['value']
            count_label_en = count_label_en + 1
        except Exception as e:
            entity_label_en = ' '
        try:
            entity_label_zh = data['labels']['zh']['value']
            count_label_zh = count_label_zh + 1
        except Exception as e:
            entity_label_zh = ' '
        #entity_label = data['labels']
        count_label = count_label + 1
        labels_id.append(str(entity_label_en) + '\t' + str(entity_label_zh) + '\t' + entity_id)
        #labels_id_missing_en.append(str(entity_label) + ' ' + entity_id)
           # break
    print("count_label_zh: " + str(count_label_zh))
    print("count_label_en: " + str(count_label_en))
    print("count_label: " + str(count_label))
    print("ratio having label_zh: " + str(count_label_zh / count_label))
    print("ratio having label_en: " + str(count_label_en / count_label))

#print(json.dumps(data, indent=4))


labels_id_file = '/home/jyu/workspace/test/out/labels_id_file.txt'
os.makedirs(os.path.dirname(labels_id_file), exist_ok=True)
with open(labels_id_file, 'w') as fout:
    fout.write('\n'.join(labels_id))

'''
labels_id_missing_en_path = '/home/jyu/workspace/test/out/id_label_missing_en.txt'
os.makedirs(os.path.dirname(labels_id_missing_en_path), exist_ok=True)
with open(labels_id_missing_en_path, 'w') as fout:
    fout.write('\n'.join(labels_id_missing_en))
'''



'''
disease_path = '/home/jyu/data/baikeMedical/nameIdMapDisease.txt'

disease_file = open(disease_path, 'r', encoding='utf-8')

lines = disease_file.readlines()
disease_file.close()

names_map = []
for line in lines:
    [disease_name, disease_id] = line.split()
    json_file_path = '/home/jyu/data/baikeMedical/jsonFiles/disease/' + disease_id
    json_file = open(json_file_path, 'r', encoding='utf-8')

    data = json.load(json_file)
    names_map.append(disease_name + " " + data["基本信息"]["英文名称"])
    json_file.close()

names_map_path = '/home/jyu/data/baikeMedical/namesMapDisease.txt'
names_map_file = open(names_map_path, 'w', encoding='utf-8')
for names in names_map:
    names_map_file.write(names)

names_map_file.close()
'''
