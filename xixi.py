from requests_html import HTMLSession, UserAgent
import re,json

session = HTMLSession()
h = session.get('https://movie.douban.com/review/best/',
                headers={'User-Agent': UserAgent().random})
     
for item in h.html.xpath('//*[@id="content"]/div/div[1]/div[1]/div'):
  print(item.find('.action span')[1].text or "0")


