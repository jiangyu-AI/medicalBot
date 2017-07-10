# ChienseMedicine
fo = open("/home/jyu/data/baikeMedical/nameIdMapChineseMedicine.txt", "r", encoding="utf-8")
lines = fo.readlines()
linesRemovedJunk = [line for line in lines if not (line[:5] == "sign=" or line[:2] == "w=" or line[:4] == "2009") ]
fo.close()

fo = open("/home/jyu/data/baikeMedical/nameIdMapChienseMedicineRemoveJunk.txt", "w", encoding="utf-8")
for line in linesRemovedJunk:
    fo.write("%s" %line)
    #print(line.encode('utf8'))
fo.close()

# medicine
fo = open("/home/jyu/data/baikeMedical/nameIdMapMedicine.txt", "r", encoding="utf-8")
lines = fo.readlines()
for line in lines:
    if (line[:2] == "w=" or line[:4] == "2009"):
        print(line.encode("utf8"))

linesRemovedJunk = [line for line in lines if not (line[:5] == "sign=" or line[:2] == "w=" or line[:4] == "2009") ]
fo.close()

fo = open("/home/jyu/data/baikeMedical/nameIdMapMedicineRemoveJunk.txt", "w", encoding="utf-8")
for line in linesRemovedJunk:
    fo.write("%s" %line)
fo.close()

# disease
fo = open("/home/jyu/data/baikeMedical/nameIdMapDisease.txt", "r", encoding="utf-8")
lines = fo.readlines()
for line in lines:
    if (line[:2] == "w=" or line[:4] == "2009"):
        print(line.encode("utf8"))

linesRemovedJunk = [line for line in lines if not (line[:5] == "sign=" or line[:2] == "w=" or line[:4] == "2009") ]
fo.close()

fo = open("/home/jyu/data/baikeMedical/nameIdMapDiseaseRemoveJunk.txt", "w", encoding="utf-8")
for line in linesRemovedJunk:
    fo.write("%s" %line)
    #print(line.encode('utf8'))
fo.close()

# treatment
fo = open("/home/jyu/data/baikeMedical/nameIdMapTreatment.txt", "r", encoding="utf-8")
lines = fo.readlines()
for line in lines:
    if (line[:2] == "w=" or line[:4] == "2009"):
        print(line.encode("utf8"))


linesRemovedJunk = [line for line in lines if not (line[:5] == "sign=" or line[:2] == "w=" or line[:4] == "2009") ]
fo.close()

fo = open("/home/jyu/data/baikeMedical/nameIdMapTreatmentRemoveJunk.txt", "w", encoding="utf-8")
for line in linesRemovedJunk:
    fo.write("%s" %line)
    #print(line.encode('utf8'))
fo.close()
