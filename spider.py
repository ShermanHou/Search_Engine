import requests
from bs4 import BeautifulSoup
from url_normalize import url_normalize
from urllib.request import urljoin 
import time
import pickle
import dill
import os
from collections import defaultdict
from collections import Counter

#url分析函数 通过requests库输入url，返回html_doc文本
def get_html_doc(url, headers = {'user-agent': 'my-app/0.0.1'}, timeout=None):
    try:
        page = requests.get(url, headers=headers, timeout=timeout)
        page.encoding = 'utf-8'
        page.raise_for_status()
        return page.text
    except:
        return None
    
# 爬取html文本中urls函数 返回urls set
def crawl_urls(html_doc, url):
    soup = BeautifulSoup(html_doc, 'html5lib')
    
    links = set()
    a_tags = soup('a')

    for i in a_tags:
        href = i.attrs.get('href')
        if(href != '' and href != None):
            if((href[-1] == 'n') or (href[-1] == 'm')):
                if not href.startswith('http'):
                    href = urljoin(url, href)
                href = url_normalize(href)
                links.add(href)
    return links

def save_variable(v, filename):
    f = open(filename, 'wb')
    pickle.dump(v, f, 0)
    f.close()
    return filename
def load_variable(filename):
    f = open(filename, 'rb')
    try: r = pickle.load(f)
    except: r = ""
    f.close()
    return r
def dill_save_variable(v, filename):
    f = open(filename, 'wb')
    dill.dump(v, f, 0)
    f.close()
    return filename
def dill_load_variable(filename):
    f = open(filename, 'rb')
    try: r = dill.load(f)
    except: r = ""
    f.close()
    return r
all_urldict = {}
loaded_urldict = True
try:
    all_urldict = load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\all_urldict.txt")
except:
    loaded_urldict = False
if all_urldict == {}:
    loaded_urldict = False
# 爬取域名下所有url对应的html文件到本地
if __name__ == '__main__':

    wait_time = 0.005
    mypath = r"C:\Users\Lenovo\Desktop\summer code\my_code\htmls"

    input_url = 'http://hqjt.ruc.edu.cn/' #输入种子url
    headers = {'user-agent': 'my-app/0.0.1'} 

    queue = [] #初始化队列 ing
    all_urlset = set() #全局urls集合，表示“出现过”
    all_urldict = {}

    queue.append(input_url)#加入queue
    all_urlset.add(input_url)#mark入全局set
    count = 0

    loaded = False
    queue_load = load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\queue.txt")
    if  queue_load != "":
        queue = queue_load
    all_urlset_load = load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\all_urlset.txt")
    if  all_urlset_load != "":
        loaded = True
        all_urlset = all_urlset_load
    count_load = load_variable("C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\count.txt")
    if  count_load != "":
        count = count_load

    while(len(queue)>0 and count<10000):
        url = queue.pop(0)#队头为最前，pop out url搜索它
        html_doc = get_html_doc(url, headers = headers)
        if html_doc is None:
            continue
        
        urls_here = crawl_urls(html_doc, url)#被搜索url的直接子节点
        for son_url in urls_here:
            if son_url in all_urlset:
                continue
            if not son_url.startswith('http://hqjt.ruc.edu.cn'):
                continue
            html_doc = get_html_doc(son_url, headers = headers)
            if html_doc == None: 
                continue
            soup = BeautifulSoup(html_doc, 'html5lib')
            if soup('p')==[] and soup(name='div',attrs={"class":"content"})==[]:
                continue
            
            count += 1
            download_path = mypath + "\{}.html".format(str(count))
            with open(download_path,'w',encoding='utf-8') as f:
                    f.write(html_doc)
                    f.close()
                    
            queue.append(son_url) #加入queue
            all_urlset.add(son_url) #mark入全局set
            all_urldict[count] = son_url

        if wait_time > 0:
            # print("等待{}秒后开始抓取".format(wait_time))
            time.sleep(wait_time)#礼貌
    if loaded == False:     
        save_variable(queue, "C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\queue.txt")
        save_variable(all_urlset,"C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\all_urlset.txt")
        save_variable(count,"C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\count.txt")
        save_variable(all_urldict, "C:\\Users\\Lenovo\\Desktop\\summer code\\my_code\\htmls\\all_urldict.txt")
