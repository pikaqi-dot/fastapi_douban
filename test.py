import json
from requests_html import HTMLSession,UserAgent
import time
import threading
import traceback
session = HTMLSession() 
user_agent = UserAgent().random 
header = {"User-Agent": user_agent}
datalist={}
datalist['movie']={}
datalist['book']={}
datalist['group']={}


def get_proxy():
    return session.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    session.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
                 

def getHtml(url):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            h = session.get(url,headers=header)
            return h
        except Exception:
            print('============',retry_count)
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None

def getTop250(url):
    global datalist
    datalist['movie']['top250']=[]
    for i in range(0,2):
        time.sleep(0.5)
        url=url+str(i*25)
        h=getHtml(url)
        for item in h.html.xpath('//*[@id="content"]/div/div[1]/ol/li'):
            data={}
            data['imgSrc']=item.xpath('//a/img')[0].attrs['src']
            data['name']=item.xpath('//a/span[1]/text()')[0]
            data['rateNum']=item.xpath('//*[@class="star"]/span[4]/text()')[0]
            datalist['movie']['top250'].append(data)
# ---------------------------------------------------------------------------------------------------
def Movie(url):
    time.sleep(0.5)
    global datalist
    h=getHtml(url)
    datalist['movie']['lists']=h.html.xpath('//*[@id="db-nav-movie"]/div[2]/div/ul/li/a/text()')
    datalist['movie']['overview']={}
    datalist['movie']['overview']['hoting']={}
    datalist['movie']['overview']['hoting']['title']=h.html.xpath('//*[@id="screening"]/div[1]/h2/text()',first=True)
    datalist['movie']['overview']['hoting']['content']=[]
    for item in h.html.xpath('//*[@class="screening-bd"]//*[@class="ui-slide-item"]')[:-2]:
        data={}
        try:
            item.find('img')
        except:
            continue
        data['title']=item.find('img',first=True).attrs['alt']
        data['imgSrc']=item.find('img',first=True).attrs['src']
        data['rating']=item.find('.subject-rate',first=True).text
        detailUrl=item.find('.poster>a',first=True).attrs['href']
        h=getHtml(detailUrl)
        data['director']=h.html.find('#info .attrs a',first=True).text
        data['actor']=h.html.xpath('//*[@id="info"]/span[2]/span[2]/span/a/text()')
        datalist['movie']['overview']['hoting']['content'].append(data)

# ----------------------------------------------------------------------------------------------------
def book(url):
    time.sleep(0.5)
    global datalist
    h=getHtml(url)
    datalist["book"]["lists"]=h.html.xpath('//*[@id="db-nav-book"]/div[2]/div/ul/li/a/text()')
# ----------------------------------------------------------------------------------------------------
def group(url):
    time.sleep(0.5)
    global datalist
    h=getHtml(url)
    datalist["group"]["lists"]=h.html.xpath('//*[@id="db-nav-group"]/div/div/div[2]/ul/li/a/text()')


def doTest():
    try: 
        getTop250('https://movie.douban.com/top250?start=')
        Movie('https://movie.douban.com/')
        book('https://book.douban.com/')
        group('https://www.douban.com/group/explore')
        with open('data.json','w') as f:
            f.write(json.dumps(datalist))
        print('++++++++++++++++++更新数据++++++++++++++++++++')
        return datalist
    except:
        print('-----------------错误:--------------------------')
        traceback.print_exc()
        return False
# def thread1():
#     while True:
#         print('-------------------开始sleep24小时--------------------')
#         time.sleep(86400)
#         doTest()
# thread_thred1 = threading.Thread(target=thread1)
# thread_thred1.start()
doTest()