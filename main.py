from flask import Flask, render_template, request  
from mycode import *
from bs4 import BeautifulSoup
app = Flask(__name__)  #实例化为app对象

@app.route('/') #接收url
def index():
    return render_template('index.html') 
def empty():
    return render_template('empty.html') 
@app.route('/query', methods = ['GET'])

def query():
    key = request.args.get('key') #用户发送的request里获取user输入的key
    key = key.replace(' ', '+')
    terms =[x for x in jieba.cut(key) if len(x) >= 1 and x not in stopwords_set and not ((x[0] >= '0' and x[0] <= '9') or (x[0] >= 'a' and x[0] <= 'z') or (x[0] >= 'A' and x[0] <= 'Z') or 
                                                                                                             (x[-1] >= '0' and x[-1] <= '9') or (x[-1] >= 'a' and x[-1] <= 'z') or (x[-1] >= 'A' and x[-1] <= 'Z')
                                                                                                             )]
    too_long = False
    if terms == []:
        return render_template('empty.html',too_long = too_long)
    if len(terms)>30:
        too_long = True
        return render_template('empty.html',too_long=too_long)
    
    # Implement your search engine here.
    # Generate a list of search results.
    ans_urls = retrieval_urls(key, 20)
    results = []
    if ans_urls == []:
        return render_template('res.html', key=key, results=results)
    for url in ans_urls:
        url_dict = {}
        title = get_h1(url)
        if title!= None:
            url_dict['title'] = title.text
        else:
            url_dict['title'] = get_title(url).text
        
        url_dict['abstract'] = query_abstract_for_url(key, url) #tuple构成的列表
        
        url_dict['url'] = url
        
        if results != []: #用title排除了重复网页
            if url_dict['title'] != results[-1]['title']:
                results.append(url_dict)
        else:
            results.append(url_dict)
    return render_template('res.html', key=key, results=results)

app.run(host='0.0.0.0', port=12345, debug=True)
#Then open [localhost:12345](http://localhost:12345) in your browser.