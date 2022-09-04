import os
import jieba
from spider import *
from bs4 import BeautifulSoup
import numpy as np

collections = [file for file in os.listdir('htmls') if os.path.splitext(file)[1] == '.html']
collections = sorted(collections, key=lambda x:int(x[:-5]))

len_collections = len(collections)

# 构造stopwords set
with open("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\stopwords.txt", 'r', encoding='utf-8') as f: 
        stopwords_list = [word.strip('\n') for word in f.readlines()]
        stopwords_set = set(stopwords_list)
        stopwords_set = stopwords_set.union('\xa0','\n','\t','!','%','--','---','----','.....','.......','........',
                                            '___________','¥','\xad','\xa0','~','|','..','°', '²', 'Ø', '\u200b', '\u200d', 
                                            '―', '•', '…', '※', '℃', '℅', 'Ⅰ', 'Ⅱ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅹ', 
                                            '√', '∩', '∶', '⼀', '\u3000', '〇', '〈', 'の', '㎡')

# 切词函数 输入某html文本soup.find指定tags后的结果,返回切好的词 list
def cuttw(whatufind):
    outwordlist = []
    for item in whatufind:
        if item.text != None:
            cut_words = [x for x in jieba.cut(item.text) if len(x) >= 1 and x not in stopwords_set and not ((x[0] >= '0' and x[0] <= '9') or (x[0] >= 'a' and x[0] <= 'z') or (x[0] >= 'A' and x[0] <= 'Z') or 
                                                                                                             (x[-1] >= '0' and x[-1] <= '9') or (x[-1] >= 'a' and x[-1] <= 'z') or (x[-1] >= 'A' and x[-1] <= 'Z')
                                                                                                             )]
            outwordlist += cut_words
    return outwordlist

# 爬取html文本标题函数 返回标题分词结果 list
def crawl_titles(html_doc):
    soup = BeautifulSoup(html_doc, 'html5lib')
    
    titles = soup.find_all("title")
    titles_h1 = soup.find_all("h1")
    titles = titles + titles_h1 
    titles_wordlist = cuttw(titles)
    return titles_wordlist
def get_title(url):
    html_doc = get_html_doc(url)
    soup = BeautifulSoup(html_doc, 'html5lib')
    return soup.find("title")
def get_h1(url):
    html_doc = get_html_doc(url)
    soup = BeautifulSoup(html_doc, 'html5lib')
    return soup.find("h1")

# 爬取html文本正文内容函数 返回标题分词结果 list
def crawl_contents(html_doc):
    soup = BeautifulSoup(html_doc, 'html5lib')
    
    contents_div = soup.find_all(name='div',attrs={"class":"content"})
    contents_p = soup.find_all('p')
    contents = contents_div +  contents_p
    contents_wordlist = cuttw(contents)
    return contents_wordlist

term_docid_pairs = []
loaded_term_docid_pairs = True
try :
    term_docid_pairs = load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\term_docid_pairs.txt")
except:
    loaded_term_docid_pairs = False
if term_docid_pairs == []:
    loaded_term_docid_pairs = False
doc_vector_length = {}
loaded_doc_vector_length = True
try :
    doc_vector_length = load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\doc_vector_length.txt")
except:
    loaded_doc_vector_length = False
if doc_vector_length == {}:
    loaded_doc_vector_length = False
    
    
#提取词-文件矩阵的所有pairs 同时计算文档空间向量长度
if __name__ == '__main__':
    if loaded_term_docid_pairs == False:
        for filename in collections:
            docid = int(filename[:-5])
            
            with open(os.path.join('htmls', filename), encoding='UTF-8') as fin:
                html_doc = fin.read()#只能read一次
                html_titles = crawl_titles(html_doc)
                html_contents = crawl_contents(html_doc)
                html_union = html_titles + html_contents ####若加权重给标题 可以在这里
                for pos, term in enumerate(html_union):#pos计数时包含了标题 0开始
                    term_docid_pairs.append((term, docid, pos))
        
                tf_log_func = np.vectorize(lambda x: 1.0 + np.log10(x) if x > 0 else 0.0, otypes = [float])
                
                term_counts = np.array(list(Counter(html_union).values()))# 计算文档对应的tf向量的长度——Counter给出tf构成的vector
                log_tf = tf_log_func(term_counts)#对数化
                doc_vector_length[docid] = np.sqrt(np.sum(log_tf**2)) #####key应该是int了
            
        save_variable(doc_vector_length, "C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\doc_vector_length.txt")
        

        term_docid_pairs = sorted(term_docid_pairs)# 默认情况下两个tuple比较大小就是先按照第一个元素比较，再按照第二个元素比较
        save_variable(term_docid_pairs, "C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\term_docid_pairs.txt")
