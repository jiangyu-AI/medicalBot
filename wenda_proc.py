#!/Python27/python
# coding=utf-8

import sys
import httplib, urllib, random, codecs
import re
import socket
import doc_proc, util

reload(sys)
sys.setdefaultencoding( "utf-8" )
from  datetime  import  *
import  time
import os.path
from urllib2 import Request, urlopen
fname_wenda = "small.tsv"
threshold = 3
STOP = ["site:", "http:", "https:", "192.168.0.1", "emoji", ".com", ".cn", "207.157", "Http",
       "ERR_CONNECTION", "http" , "192.168", "DNS_PROBE_POSSIBLE", "ERR_CONNECTION_RESET", "weixin:"
        "dll", "作文"]
MAX_COUNT_Q = 50
MIN_COUNT_Q = 3
DATA_ROOT = "/Workspace/data/wenda/"
ROOT = DATA_ROOT + "crawler/3/"

def crawl_urls():
    socket.setdefaulttimeout(5.0)
    with open("C:\\Workspace\\Data\\wenda\\crawler\\baiduurl.txt", "r") as fp:
        urls = fp.readlines()
        idx = 0
        for url in urls:
            if idx % 100 == 0:
                print  datetime.now(), " working on " , idx , url
            idx += 1
            url = url.strip()
            if len(url) == 0:
                continue
            output_fname = get_fname(url)
            if os.path.isfile(ROOT + output_fname):
                continue
            try:
                crawl_url(url)
            except Exception, e:
                print "exception on ", url, e
                time.sleep(1)
                continue
                #sys.exit(1)
            time.sleep(0.3 + random.uniform(0.1, 0.3))


def crawl_url(url): #'https://zhidao.baidu.com/question/1950376213182271028.html'
    q = Request(url)
    q.add_header('Content-Type', 'text/html')
    ''' q.add_header('Content-Encoding', 'gzip, deflate, sdch, br')
    q.add_header('Server', 'Apache')
    q.add_header('Transfer-Encoding', 'chunked')
    q.add_header('Vary', 'Accept-Encoding')
    q.add_header('Wait', '2')
    q.add_header('Date', datetime.now())
    q.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36')
    q.add_header('Host', 'zhidao.baidu.com')
    q.add_header('Accept-Language', 'en-US,en;q=0.8,zh-CN;q=0.6')
    q.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')'''
    fail = 0
    while True:
        if fail >3:
            break
        try:
            content = urlopen(q).read()
        except:
            print("exception retry ", url )
            fail += 1
        else:
            break
    output_fname = get_fname(url)
    with open(ROOT + output_fname, "w") as f:
        f.write(content)

def get_fname(url):
    vals = url.split("/")
    output_fname = vals[len(vals) - 1]
    output_fname = output_fname.replace("?", "")
    output_fname = output_fname.replace("&", "")
    return output_fname

def fiterQuery():
    fname_wd = "wenda_q2q.dat"
    fname_filter = "topclicked.txt"

    query_dict = set()
    dedup = set()
    with open(fname_filter, "r" ) as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip()
            if len(line) >= MAX_COUNT_Q or len(line) <= MIN_COUNT_Q:
                continue
            query_dict.add(line)

    result = []
    index = 0
    with codecs.open(fname_wd, "r", encoding="GB18030" ) as fp:
        lines = fp.readlines()
        for line in lines:
            index += 1
            skip = False
            for st in STOP:
                if st in line:
                    skip = True
                    break
            if skip:
                continue
            line = line.strip()
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace(" ", "")
            if len(line) <= 1:
                continue

            vals = line.split("\t")

            try:
                w0 = vals[0]
                w1 = vals[1]
            except Exception as e:
                print index,line, e
                pass

            if clean(w0) == clean(w1):
                continue
            if len(w1) >= MAX_COUNT_Q or len(w0) >= MAX_COUNT_Q or len(w1) <= MIN_COUNT_Q or len(w0) <= MIN_COUNT_Q:
                continue
            if not w0 in query_dict and not w1 in query_dict:
                continue
            if w0 in dedup or w1 in dedup:
                continue
            dedup.add(w0)
            dedup.add(w1)
            result.append(w0+"\t"+w1)

    with open ("filtered/wenda_filtered.tsv", "w") as fw:
        str = "\n".join(result)
        #change_encoding(str, "utf-8", "gbk")
        fw.write(str)
    print("done writing wenda_filtered.tsv")


def change_encoding(str, efr, eto):
    try:
        str=str.decode(efr)
        str = str.encode(encoding=eto)
    except Exception as e:
        str=str.decode("gbk")
        str = str.encode(encoding=eto)
    return str


punc = ["?", ",", "!"]
def clean(str):
    for p in punc:
        if p in str:
            str = str.replace(p, "")
    return str


def extend():
    with open("wenda_q2q.seq3", "w") as fw:
        with codecs.open("wenda_q2q.seg", "r", "utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                fw.write(line.strip() + "\t1\n" )


def iconv(f1, f2, enfrom="utf-8", ento="gbk"):
    with open(f2, "w") as fw:
        lines= util.readlines_from_file(f1)
        for line in lines:
            #line = line.strip().replace(" ", ",").replace("\n", ",") + "\n"
            line = re.sub(",+", ",", line)
            #if not "\t" in line or len(line) == 1 or line.count("\t") > 1:
            #    continue
            try:
                s = change_encoding(line, enfrom, ento)
            except Exception as e:
                print(e.message, line)
                continue
            fw.write(s + "\n")

if __name__=="__main__":
    #crawl_url("https://zhidao.baidu.com/list?pn=270&rn=30&_pjax=%23j-question-list-pjax-container&type=hot&cid=113128")
    #fiterQuery()
    #crawl_urls()
    iconv("C:\\Workspace\\Data\\active_learning\\zhao\\xingren\\xingren.gbk.seg.q",
          "C:\\Workspace\\Data\\active_learning\\zhao\\xingren\\xingren.utf8.seg.q", "gbk", "utf-8")
    #iconv("C:\\Workspace\\Data\\wenda\\data\\testseg.txt", "C:\\Workspace\\Data\\wenda\\data\\testseggb.txt")
    #iconv("filtered/zhidao_posneg/baidu_qqpos.tsv", "filtered/zhidao_posneg/baidu_pos_gb.tsv")
    #extend()
