
wiki_labels_id_file = '/home/jyu/data/wiki/labels_id.txt'
baike_names_id_file = '/home/jyu/data/baikeMedical/nameIdMapDisease.txt'#'/home/jyu/data/baikeMedical/names_id.txt'

with open(wiki_labels_id_file) as wiki_file:
    wiki_labels_id = wiki_file.readlines()

with open(baike_names_id_file) as baike_file:
    baike_names_id = baike_file.readlines()
    
labelEn_id_dic = {}
labelCh_id_dic = {}

for labels_id in wiki_labels_id:
    labels_id_splited = labels_id.split('\t')
    if(len(labels_id_splited) != 3):
        print(labels_id)
        continue
    labelEnRaw, labelChRaw, wiki_id = labels_id_splited
    labelEn = labelEnRaw.lower()
    labelCh = labelChRaw.lower()
    if labelEn.strip() != '':
        labelEn_id_dic[labelEn] = wiki_id
    if labelCh.strip() != '':
        labelCh_id_dic[labelCh] = wiki_id

#matches_by_nameEn = []
matches_by_nameCh = []

for names_id in baike_names_id:
    try:
        nameCh, baike_id = names_id.split()
    except:
        print(names_id)
    #nameEn = nameEnRaw.lower()

    if nameCh in labelCh_id_dic:
        wiki_id = labelCh_id_dic[nameCh]
        matches_by_nameCh.append(baike_id.strip('\n') + '\t' + wiki_id.strip('\n') + '\t' + nameCh)


matches_by_nameCh_file = '/home/jyu/data/disease_matches_by_nameCh.txt'

'''
with open(matches_by_nameEn_file, 'w') as f:
    f.write('\n'.join(matches_by_nameEn))
'''

with open(matches_by_nameCh_file, 'w') as f:
    f.write('\n'.join(matches_by_nameCh))
