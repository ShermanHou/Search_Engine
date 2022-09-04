import os
import jieba
from bs4 import BeautifulSoup
import numpy as np
from cmath import log10
from spider import *
from make_pairs import *
from make_dict import *

def get_key(url):
    for k, v in all_urldict.items():
        if v == url:
            return k
    return None

# 保存网页的纯文本文件
if __name__ == '__main__':
    mypath2 = r"C:\Users\Lenovo\Desktop\summer code\my_code\real_html_words"
    loaded_real_html_words = True
    if loaded_real_html_words == False:
        for filename in collections:
            docid = int(filename[:-5])
            with open(os.path.join('htmls', filename), encoding='UTF-8') as fin:
                    html_doc = fin.read()#只能read一次
                    soup = BeautifulSoup(html_doc)
                    contents_div = soup.find_all(name='div',attrs={"class":"content"})
                    contents_p = soup.find_all('p')
                    contents_tags = contents_div + contents_p
                    contents = ''
                    for tag in contents_tags:
                        contents += tag.text    
                    # words = list(jieba.tokenize(contents))
                    download_path2 = mypath2 + "\{}.txt".format(str(docid))
                    with open(download_path2,'w',encoding='utf-8') as f:
                            f.write(contents)
                            f.close()