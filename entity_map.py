import json
import gzip

wiki_13g_path = '/home/jyu/data/wiki/wikidata-20170703-all.json.gz'
with gzip.p

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
