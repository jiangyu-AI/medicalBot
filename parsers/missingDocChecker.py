from io import BytesIO
import os

missingFiles = []
with open("/home/wechaty/data/webpages/diseaseNameIdMap.txt", 'r', encoding='utf-8') as f:
    for line in f:
        nameId = line.split(" ")
        name = nameId[0].encode('utf-8')
        fileName = os.path.join(u"/home/wechaty/data/jsonFiles/disease/".encode('utf-8'), name)
        if not os.path.exists(fileName):
            missingFiles.append(u"http://baike.baidu.com/item/".encode('utf-8') + name + u"/".encode('utf-8') + nameId[1].encode('utf-8'))

with open("/home/wechaty/data/diseaseMissingFiles.txt", 'wb') as f:
    for ele in missingFiles:
        f.write(ele)

