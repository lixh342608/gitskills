#coding=utf-8
'''
Created on 2017年6月16日

@author: Administrator
'''

import requests,re,json
from bs4 import BeautifulSoup

res=requests.get('https://jr.yatang.cn//Financial/getAssetList?&p=1')

t_text=json.loads(res.text)['list']


for i in t_text:
    
    t_text.remove(i)
    
print(t_text)

