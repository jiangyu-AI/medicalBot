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
