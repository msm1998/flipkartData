from urllib.request import Request,urlopen,urlretrieve
from urllib.error import URLError,HTTPError
from bs4 import BeautifulSoup
from pprint import pprint
from collections import defaultdict,OrderedDict,namedtuple
import re
import os
url='http://flipkart.com'
inp = input()
req = url+'/search?q='+inp
print(req)
path = "/home/pc/flipcartData/" + inp
try:
    if os.path.exists(path):
        print("already exists")
    else:
        os.mkdir(path)
        print("successfully created dir %s "% path)
except OSError:
    print("creation of dir failed")



def connection(pages):
    if str(pages).isdigit():
        response = urlopen(req+"&page="+str(pages))
    else:
        response = urlopen(url) 
    return BeautifulSoup(response.read(),'lxml')

try:
    products = []
    d=namedtuple('product',['pro_brand','pro_name','pro_price','link'])
    for pages in range(0,1):
        data = connection(pages)
        product_list = data.findAll("div",{"class":"IIdQZO _1SSAGr"})
        for i in product_list:
            data = i.find("div",{"class":"_2LFGJH"})
            price = data.find("div",{"class":"_1vC4OE"})
            img = i.find("div",{"class":"_3ZJShS _31bMyl"})
            subdir = path+"/"+data.a['title']+"_"+data.div.text+"_"+price.text
            if os.path.exists(subdir):
                print(subdir+" is already there.")
            else:
                res = urlopen(url+data.a['href'])
                imgdata = BeautifulSoup(res.read(),'lxml')
                os.mkdir(subdir)
                os.chdir(subdir)
                ul = imgdata.findAll("li",{"class":"_4f8Q22 _2y_FdK _3_yGjX"})
                m=0
                for j in ul:
                    k = j.find("div",{"class":"_2_AcLJ _3_yGjX"})['style']
                    img_link = k[k.find('(')+1 : k.find(')')].replace('128/128','800/900',1)
                    print(img_link)
                    img_name=str(m)+".jpg"
                    m+=1
                    urlretrieve(img_link,img_name)
                print("---------------------")
except HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
except URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
    
