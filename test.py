import json
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
def Movie(url):
  time.sleep(0.5)
  global datalist
  h = getHtml(url)
  datalist['movie']['lists'] = h.html.xpath(
    '//*[@id="db-nav-movie"]/div[2]/div/ul/li/a/text()')
  datalist['movie']['overview'] = {}
  datalist['movie']['overview']['hoting'] = {}
  datalist['movie']['overview']['hoting']['title'] = h.html.xpath(
    '//*[@id="screening"]/div[1]/h2/text()', first=True)
  datalist['movie']['overview']['hoting']['content'] = []
  for item in h.html.xpath(
      '//*[@class="screening-bd"]//*[@class="ui-slide-item"]')[:-2]:
    data = {}
    try:
      item.find('img')
    except:
      continue
    data['title'] = item.find('img', first=True).attrs['alt']
    data['imgSrc'] = item.find('img', first=True).attrs['src']
    data['rating'] = item.find('.subject-rate', first=True).text
    detailUrl = item.find('.poster>a', first=True).attrs['href']
    h = getHtml(detailUrl)
    data['director'] = h.html.find('#info .attrs a', first=True).text
    data['actor'] = h.html.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    ratingNum=h.html.find('.rating_people>span')
    data['ratingNum']=(len(ratingNum) and ratingNum[0].text) or "无"
    datalist['movie']['overview']['hoting']['content'].append(data)
    


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
    getTop250('https://movie.douban.com/top250?start=')
    Movie('https://movie.douban.com/')
    book('https://book.douban.com/')
    group('https://www.douban.com/group/explore')
    with open('data.json', 'w') as f:
      f.write(json.dumps(datalist))
    print('\033[32m++++++++++++++++++更新数据++++++++++++++++++++\033[0m')
    return datalist
  except:
    print(
      '\033[31m+----------------------错误:--------------------------+\033[0m')
    print('\033[33m{}\033[0m'.format(traceback.print_exc()))
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
