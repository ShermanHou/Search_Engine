from mycode import *
def evaluate(query):
    url_list = retrieval_urls(query, 20)
    assert len(url_list) == 20
    return url_list
