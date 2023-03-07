import json,re,os
from requests_html import HTMLSession, UserAgent
import time
# import threading
import traceback

session = HTMLSession()
user_agent = UserAgent().random
header = {"User-Agent": user_agent}
datalist = {}
datalist['movie'] = {}
datalist['book'] = {}
datalist['group'] = {}

def getHtml(url):
  h = session.get(url, headers=header)
  if (h.status_code == 200):
    return h
  return None
  
def getTop250(url):
  global datalist
  datalist['movie']['top250'] = []
  for i in range(0, 2):
    time.sleep(0.5)
    url = url + str(i * 25)
    h = getHtml(url)
    for item in h.html.xpath('//*[@id="content"]/div/div[1]/ol/li'):
      data = {}
      data['imgSrc'] = item.xpath('//a/img')[0].attrs['src']
      data['name'] = item.xpath('//a/span[1]/text()')[0]
      data['rateNum'] = item.xpath('//*[@class="star"]/span[4]/text()')[0]
      datalist['movie']['top250'].append(data)

# ---------------------------------------------------------------------------------------------------
def movie(url):
  time.sleep(0.5)
  global datalist
  h1 = getHtml(url)
  datalist['movie']['lists'] = h1.html.xpath(
    '//*[@id="db-nav-movie"]/div[2]/div/ul/li/a/text()')
  datalist['movie']['overview'] = {}
  datalist['movie']['overview']['hoting'] = {}
  datalist['movie']['overview']['hoting']['title'] = h1.html.xpath(
    '//*[@id="screening"]/div[1]/h2/text()', first=True)
  datalist['movie']['overview']['hoting']['content'] = []
  for item in h1.html.xpath(
      '//*[@class="screening-bd"]//*[@class="ui-slide-item"]')[:-2]:
    data = {}
    f=item.find('img',first=True)
    try:
      a=f.attrs
    except:
      continue
    
    data['title'] = f.attrs['alt']
    data['imgSrc'] = f.attrs['src']
    data['rating'] = item.find('.subject-rate', first=True).text
    detailUrl = item.find('.poster>a', first=True).attrs['href']
    h2 = getHtml(detailUrl)
    data['director'] = h2.html.find('#info .attrs a', first=True).text
    data['actor'] = h2.html.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    ratingNum=h2.html.find('.rating_people>span')
    data['ratingNum']=(len(ratingNum) and ratingNum[0].text) or "无"
    data['date']=h2.html.xpath('//*[@id="content"]/h1/span[2]/text()',first=True)
    movie_time=h2.html.xpath('//*[@id="info"]/*[@property="v:runtime"]/text()')
    data['time']=(len(movie_time) and movie_time[0]) or "暂无此信息"
    data['area']=re.findall("制片国家/地区: (.*?)',",str( h2.html.find('.article #info')[0].text.split('\n')))[0]
    datalist['movie']['overview']['hoting']['content'].append(data)
  datalist['movie']['overview']['hoting']['pinglun']=[]
  for item in h1.html.xpath('//*[@id="reviews"]/div[2]/div'):
    data={}
    data['imgSrc']=item.find('img')[0].attrs['data-original']
    data['title']=item.find('.review-bd>h3>a')[0].text
    data['name']=item.find('.review-bd>.review-meta>a:nth-child(1)')[0].text
    data['movieName']=item.find('.review-bd>.review-meta>a:nth-child(2)')[0].text
    data['star']=item.find('.review-bd>.review-meta>span')[0].search('<span class="allstar{}"/>')[0]
    data['content']=re.findall('(.*?)... \(全文\)',item.find('.review-content')[0].text)[0]
    datalist['movie']['overview']['hoting']['pinglun'].append(data)
  movieReview()

    
def movieReview():
  h=getHtml('https://movie.douban.com/review/best/')
  global datalist
  datalist['movie']['reviewBest']=[]
  for item in h.html.xpath('//*[@id="content"]/div/div[1]/div[1]/div'):
    data={}
    data['imgSrc']=item.find('.subject-img img')[0].attrs['src']
    data['userImgSrc']=item.find('.main-hd img')[0].attrs['src']
    data['userName']=item.find('.main-hd .name')[0].text
    try:
      data['star']=item.find('.main-hd span:nth-of-type(1)')[0].search('<span class="allstar{} main-title-rating"')[0]
    except:
      data['star']="50"
    data['date']=item.find('.main-meta')[0].text
    data['title']=item.find('.main-bd>h2>a')[0].text
    data['content']=re.findall('(.*?)\xa0\(展开',item.find('.short-content')[0].text)[0]
    rate=item.find('.action span')
    data['upRate']=rate[0].text or "0"
    data['downRate']=rate[1].text or "0"
    data['reply']=item.find('.reply')[0].text
    datalist['movie']['reviewBest'].append(data)
    

#，非主动抓取，等待用户调用。一个用户调用一个任何人也没有抓取过的页面信息，会开始抓取并持久化到文件。24小时后删除，等待用户主动调用。
def getMoreMovieReview(page:int):
  try:
    h=session.get('https://movie.douban.com/review/best/?start={}'.format(str((page-1)*20)),headers={'User-Agent': UserAgent().random})
    try:
      h.html.xpath('//*[@id="content"]/div/div[1]/div[1]/div')[0]
    except:
      print('\033[31m+-------------------抓取未爬取的评论页第{}页错误:爬虫已被禁！--------------+\033[0m'.format(page))
      print(traceback.print_exc())
      print('\033[31m+-------------------------------------------------------------------------+\033[0m')
      return False
    pageData=[]
    for item in h.html.xpath('//*[@id="content"]/div/div[1]/div[1]/div'):
      data={}
      data['imgSrc']=item.find('.subject-img img')[0].attrs['src']
      data['userImgSrc']=item.find('.main-hd img')[0].attrs['src']
      data['userName']=item.find('.main-hd .name')[0].text
      try:
        data['star']=item.find('.main-hd span:nth-of-type(1)')[0].search('<span class="allstar{} main-title-rating"')[0]
      except:
        data['star']="50"
      data['date']=item.find('.main-meta')[0].text
      data['title']=item.find('.main-bd>h2>a')[0].text
      data['content']=re.findall('(.*?)\xa0\(展开',item.find('.short-content')[0].text)[0]
      rate=item.find('.action span')
      data['upRate']=rate[0].text or "0"
      data['downRate']=rate[1].text or "0"
      data['reply']=item.find('.reply')[0].text
      pageData.append(data)
    fileName="MovieReview"+str(page)
    if(not os.path.exists("movieReviewPage")):
      os.mkdir("movieReviewPage")
    with open("movieReviewPage/{}".format(fileName),'w') as f:
      f.write(json.dumps(pageData))
    print('pageData:',pageData)
    return pageData
    
  except:
    print('\033[31m+----------------------抓取评论页{}错误:--------------------------+\033[0m'.format(page))
    print(traceback.print_exc())
    print('\033[31m+------------------------------------------------------------+\033[0m')
    return False
  
  
  
    
    
    
  
  
    
    


# ----------------------------------------------------------------------------------------------------
def book(url):
  time.sleep(0.5)
  global datalist
  h = getHtml(url)
  datalist["book"]["lists"] = h.html.xpath(
    '//*[@id="db-nav-book"]/div[2]/div/ul/li/a/text()')


# ----------------------------------------------------------------------------------------------------
def group(url):
  time.sleep(0.5)
  global datalist
  h = getHtml(url)
  datalist["group"]["lists"] = h.html.xpath(
    '//*[@id="db-nav-group"]/div/div/div[2]/ul/li/a/text()')


def doTest():
  try:
    movie('https://movie.douban.com/')
    getTop250('https://movie.douban.com/top250?start=')
    book('https://book.douban.com/')
    group('https://www.douban.com/group/explore')
    with open('data.json', 'w') as f:
      f.write(json.dumps(datalist))
    print('\033[32m++++++++++++++++++更新数据++++++++++++++++++++\033[0m')
    return datalist
  except:
    print(
      '\033[31m+----------------------错误:--------------------------+\033[0m')
    traceback.print_exc()
    print(
      '\033[31m+-----------------------------------------------------+\033[0m')
    return False


# def thread1():
#     while True:
#         print('\33[32m-------------------开始sleep24小时--------------------\33[0m')
#         time.sleep(86400)
#         doTest()
# thread_thred1 = threading.Thread(target=thread1)
# thread_thred1.start()
