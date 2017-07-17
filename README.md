1st floor printer: 
10.3.5.52



17765

航空航天 
(共463个)汽车工程 
(共1341个)生物医学 
(共251个)环境科学 
(共497个)气象科技 
(共295个)水产养殖 
(共1479个)食品科技 
(共1075个)通信科技 
(共3634个)水利科学 
(共1382个)核能利用 
(共1351个)体育科学 
(共1391个)力学 
(共1042个)化工科技 
(共1754个)电子信息 
(共1810个)心理健康 
(共935个)




baike science data is completed: 
location: 228   /home/jyu/data/baike/ 
number of files:  40605
size: 3.4G (html)  316M jsonfiles





num of files in science:
[463, 1340, 251, 497, 295, 1478, 1072, 3630, 1382, 1350, 1388, 1040, 1754, 1807, 933, 7251, 8155, 4105, 2417]
>>> sum(nums)
40608
jyu@yu:~/workspace/medicalBot$ find ~/data/baikeFive/science/. -type f | wc -l
40662

find /home/jyu/data/baikeFive/jsonFiles0/. -type f |wc -l
40605

num of files in bfs new files: 
wc -l /home/jyu/data/baikeFive/urlsBfsNew.txt
78975 /home/jyu/data/baikeFive/urlsBfsNew.txt



matches between baike names and wiki labels

413 matches_by_nameEn.txt
1638 matches_by_nameCh.txt
matches ratio: by nameCh
>>> 1638/24382
0.0671807070789927

baike sstats:
count_total: 24382 baikeMedical/names_id.txt
ratio having Englsh name: < 6%

wiki stats:
count_total: 27827809 wiki/labels_id.txt
count_label_zh: 1528208
count_label_en: 16616047
ratio having label_zh: 0.05491657446274069
ratio having label_en: 0.5971022153737574




great Traditional Chinese and simplified Chinese converter: 

https://pypi.python.org/pypi/hanziconv


# medicalBot
5 July: map id between wiki data and baiduBaike data



install virtualenvwrapper: 

http://exponential.io/blog/2015/02/10/install-virtualenv-and-virtualenvwrapper-on-ubuntu/

Step-by-step instructions

Open a terminal and install the following packages.

sudo apt-get install python-pip python-dev build-essential

sudo pip install virtualenv virtualenvwrapper

sudo pip install --upgrade pip

Setup virtualenvwrapper in ~/.bashrc.

# Create a backup of your .bashrc file
cp ~/.bashrc ~/.bashrc-org

# Be careful with this command
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' \
'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc

Enable the virtual environment.

source ~/.bashrc

mkdir -p $WORKON_HOME

mkvirtualenv api

# Exit the 'api' virtual environment
deactivate

Tips on using virtualenv

To enable the api virtual environment, run the following command:

workon api

To deactivate the api virtual environment, run the following command:

deactivate




1, crawl and parse the following four websites for medical pages. 
http://baike.baidu.com/wikitag/taglist?tagId=75953
科学百科疾病症状分类(共7252个)

http://baike.baidu.com/wikitag/taglist?tagId=75954
科学百科药物分类(共8155个)

http://baike.baidu.com/wikitag/taglist?tagId=75956
科学百科中医药分类(共4105个)

http://baike.baidu.com/wikitag/taglist?tagId=75955
科学百科诊疗方法分类(共2418个)

In total: 21930

2,

http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
count number of files: 
grep -Rl "curl" ./ | wc -l

data json file format:
{"title":{
         "summary":"...",
         "cause":"...",
         "treatment":"..."
    }
}

{"data":[{"title":"XXX", "paragraphs":[{"context":"", "qas":[
    {"answers":[{"answer_start":255, "text":"west"}], "question":"YYY?", "id":"5735cc33012e2f140011a069"}, 
    {"answers":[{"answer_start":255, "text":"west"}], "question":"YYY?", "id":"5735cc33012e2f140011a069"}, 
    
    ]}]}]}

// solution for writing and displaying Chinase
Setting the Default Java File Encoding to UTF-8:

    export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8

server.228

git
jira

codeReview
unitTest
