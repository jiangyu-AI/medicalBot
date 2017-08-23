#import edu.stanford.nlp.process.DocumentPreprocessor
from nltk.tokenize import sent_tokenize
import json

data_squad_train = '/home/jyu/data/squad/train-v1.1.json'

with open(data_squad_train) as f:
  data = json.load(f)
#for key in data.keys():
#  print(key)

article_list = data['data']
for article in article_list:
  for paragraph in article['paragraphs']:
    context = paragraph['context'] 
    sent_tokenize_list = sent_tokenize(context)
    print(context)
    print('sent_tokenize_list')
    for sent_tokenize in sent_tokenize_list:
      print(sent_tokenize)
    break 
  break
