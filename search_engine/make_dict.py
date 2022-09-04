import os
import jieba
from bs4 import BeautifulSoup
import numpy as np
from cmath import log10
from spider import *
from make_pairs import *
class Posting(object):
    special_doc_id = -1
    def __init__(self, docid, tf=0, idf=0, pos_list = []):
        self.docid = docid
        self.tf = tf
        self.idf = idf
        self.pos_list = pos_list
    def __repr__(self):
        return "<docid: %d, tf: %d>" % (self.docid, self.tf)
postings_dict = {}
loaded_postings_dict = True
try :
    postings_dict = dill_load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\postings_dict.txt")
except:
    loaded_postings_dict = False
if postings_dict == {}:
        loaded_postings_dict = False
        
if __name__ == '__main__':
    if loaded_postings_dict == False:
        postings_dict = defaultdict(lambda: [Posting(Posting.special_doc_id, 0)]) #list
        
        for term, docid, pos in term_docid_pairs: #核心是遍历term，后两个值为其附属
            postings_list = postings_dict[term] #default形式添加键值对，并给新建的值贴标签为postings_list
            if docid != postings_list[-1].docid:
                postings_list.append(Posting(docid, 1, pos_list = [pos]))
            else:
                postings_list[-1].tf += 1
                postings_list[-1].pos_list.append(pos)
                
        for key, value in postings_dict.items():
            df = len(postings_dict[key])
            idf = log10(len_collections/len(postings_dict[key]))
            for post in value:
                # if df <= 15:
                #     post.idf = 5 * idf
                # elif df <= 45:
                #     post.idf = 3 * idf
                # else:
                post.idf = idf
                
        postings_dict = dict(postings_dict) #defaultdict to dict
        
        dill_save_variable(postings_dict, "C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\postings_dict.txt")
