import os
import jieba
from bs4 import BeautifulSoup
import numpy as np
from cmath import log10
from spider import *
from make_pairs import *
from make_dict import *

# 查询函数 输入term词，输出docids构成的列表（如果用collections取文件名要注意索引错位） list
def query_docid(query_term):
    try:
        postings_list = postings_dict[query_term][1:] # 删去开头的-1
        results = [posting.docid for posting in postings_list]
        return results
    except:
        return []
    
def query_postings_list(query_term):
    try:
        return postings_dict[query_term][1:]
    except KeyError:
        return []
def query_list_of_pos_list(query_term):
    try:
        postings_list = postings_dict[query_term][1:] # 删去开头的-1
        results = [posting.pos_list for posting in postings_list]
        return results
    except:
        return []

def docid_list_to_url_list(good_docid_list):
    url_list = []
    for docid in good_docid_list:
        url_list.append(all_urldict[docid])
    return url_list   

def query_urls(query_term):
    return docid_list_to_url_list(query_docid(query_term))

# 检查是否完整包含query函数 输出bool
def full_matching_phrase_docid(query):
    ans_list = []
    query_terms = [x for x in jieba.cut(query) if len(x) >= 1 and x not in stopwords_set and not ((x[0] >= '0' and x[0] <= '9') or (x[0] >= 'a' and x[0] <= 'z') or (x[0] >= 'A' and x[0] <= 'Z') or 
                                                                                                             (x[-1] >= '0' and x[-1] <= '9') or (x[-1] >= 'a' and x[-1] <= 'z') or (x[-1] >= 'A' and x[-1] <= 'Z')
                                                                                                             )]
    query_len = len(query_terms)
    query_terms_docidlist = [query_docid(term) for term in query_terms]
    now_index = 1 #==正在检验的词的index
    
    term_polistlist = query_list_of_pos_list(query_terms[0]) #起始词的polistlist
    for order, pos_list in enumerate(term_polistlist):
        now_docid = query_terms_docidlist[0][order] #记录检索到含起始词的哪个docid了
        refer_pos_list = term_polistlist[order]
        for pos in refer_pos_list:
            if checknext(now_docid, now_index, query_terms, query_terms_docidlist, refer_pos_list, pos):
                # print(pos)
                if now_docid not in ans_list:
                    ans_list.append(now_docid)
                # return ans_list
            else:
                continue
    return ans_list
#在既定docid里，在既定pos处，后词的列表是否能对应上
def checknext(now_docid, now_index, query_terms, query_terms_docidlist, refer_pos_list, now_pos):
    if now_index == len(query_terms):
        return True
    check_term_docid_list = query_terms_docidlist[now_index]
    if now_docid not in check_term_docid_list: 
        return False
    
    index_of_docid_in_purpose_term = query_terms_docidlist[now_index].index(now_docid)
    check_pos_list = query_list_of_pos_list(query_terms[now_index])[index_of_docid_in_purpose_term]
    purpose_pos = now_pos + 1
    if purpose_pos in check_pos_list:
        # print(query_terms[now_index])
        return checknext(now_docid, now_index+1, query_terms, query_terms_docidlist, refer_pos_list, purpose_pos)
    else:
        return False
    
#计算余弦相似度
def cosine_scores(query):
    scores = defaultdict(lambda: 0.0)  # 保存分数
    query_terms = Counter([x for x in jieba.cut(query) if len(x) >= 1 and x not in stopwords_set and not ((x[0] >= '0' and x[0] <= '9') or (x[0] >= 'a' and x[0] <= 'z') or (x[0] >= 'A' and x[0] <= 'Z') or 
                                                                                                             (x[-1] >= '0' and x[-1] <= '9') or (x[-1] >= 'a' and x[-1] <= 'z') or (x[-1] >= 'A' and x[-1] <= 'Z')
                                                                                                             )])#######################
    tf_log_func = np.vectorize(lambda x: 1.0 + np.log10(x) if x > 0 else 0.0, otypes = [float])
    for q in query_terms:
        w_tq = tf_log_func(query_terms[q])
        postings_list = query_postings_list(q)
        for posting in postings_list:
            w_td = (tf_log_func(posting.tf)) * (posting.idf)
            scores[posting.docid] += w_td * w_tq + 3
        # print(q)
            
    # results = [(docid, score / doc_vector_length[docid])
    results = [(docid, score )
               for docid, score in scores.items() ]
    results.sort(key=lambda x: -x[1])
    return results

def final_scores(query,k=20):
    full_matching_phrase_docid_list = full_matching_phrase_docid(query)
    cosine_scores_results = cosine_scores(query)
    
    final_results = []
    # print(len(cosine_scores_results))
    if(len(cosine_scores_results)>25):
        for pair in cosine_scores_results[0:25]:
            if pair[0] in full_matching_phrase_docid_list:
                final_results.append((pair[0], pair[1] * 1e10))
            else:
                final_results.append(pair)
                
    if(len(cosine_scores_results)<=25):
        for pair in cosine_scores_results:
            if pair[0] in full_matching_phrase_docid_list:
                final_results.append((pair[0], pair[1] * 1e10))
            else:
                final_results.append(pair)
                
                
    final_results.sort(key=lambda x: -x[1])
    
    if final_results == []:
        return []
    if len(final_results) < 20:
        while(len(final_results) < 20):
            final_results.append(final_results[-1])
            
    return final_results[0:k]


def i_want_you(query):
    return [all_urldict[x] for x in full_matching_phrase_docid(query) ]

def retrieval_urlscore(query, k=20):
    top_scores = final_scores(query, k=k)
    results = [(all_urldict[docid], score) for docid, score in top_scores]
    return results

def retrieval_urls(query, k=20):
    top_scores = final_scores(query, k=k)
    results = [all_urldict[docid] for docid, score in top_scores]
    return results