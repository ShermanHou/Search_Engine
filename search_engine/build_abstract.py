import os
import jieba
from bs4 import BeautifulSoup
import numpy as np
from cmath import log10
from spider import *
from make_pairs import *
from make_dict import *
from save_pure import *
from score_rank import *

# 返回带有关键词标记的词列表
def query_abstract_for_url(query, url): 
    query_terms = [x for x in jieba.cut(query) if x != ' ']
    abstract_word_num = 90 #词数固定，len不固定
    docid = get_key(url)
    with open(os.path.join(mypath2,'{}.txt'.format(str(docid))), encoding='UTF-8') as fin: #可以自动加\\诶
            contents = fin.read()#只能read一次 
    words = [x for x in jieba.cut(contents)  if x != '\n' and x != '\r' and x != '\t' and x != ' ' and x != '\r\n' and x != '\n\r']
    contents_word_num = len(words)
    
    max_contain = [(0,0)]
    for start_word_num in range(max(0,contents_word_num - abstract_word_num)):
        window_words = []
        for now_pick_num in range(abstract_word_num):
            window_words.append(words[now_pick_num+start_word_num])
            
        contain_num = 0
        for term in query_terms:
            if term in window_words:
                contain_num += 1
        if contain_num == len(query_terms):
            max_contain = [(start_word_num, contain_num)]
            break
        if contain_num >= max_contain[0][1]:
            max_contain = [(start_word_num, contain_num)]
    real_start_num = max(0, max_contain[0][0] - 2)
    real_end_num = min(contents_word_num, max_contain[0][0] + abstract_word_num+2)
    abstract_window = []
    for k in range(real_start_num, real_end_num):
            if words[k] in query_terms and words[k] not in stopwords_list:
                abstract_window.append((words[k], 1))
            else:
                abstract_window.append((words[k], 0))
    return abstract_window