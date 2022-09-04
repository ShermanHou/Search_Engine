import os
import jieba
from bs4 import BeautifulSoup
import numpy as np
from cmath import log10
from score_rank import *

print(retrieval_urlscore('人大幼儿园坚持文化立园'))