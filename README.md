# medicalBot
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


Setting the Default Java File Encoding to UTF-8:

    export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8

server.228

git
jira

codeReview
unitTest
