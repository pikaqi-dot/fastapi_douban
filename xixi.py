from requests_html import HTMLSession, UserAgent
import re,json,os

session = HTMLSession()
# h = session.get('https://movie.douban.com/review/best/',
#                 headers={'User-Agent': UserAgent().random})
     

def getMoreMovieReview(page):
  h=session.get('https://movie.douban.com/review/best/?start={}'.format(int(page-1)*20),headers={'User-Agent': UserAgent().random})
  fileName="MovieReview"+str(page)
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
  if(not os.path.exists("movieReviewPage")):
    os.mkdir("movieReviewPage")
  with open("movieReviewPage/{}".format(fileName),'w') as f:
    f.write(json.dumps(pageData))

getMoreMovieReview(2)