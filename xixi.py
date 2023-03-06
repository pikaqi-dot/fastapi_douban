from requests_html import HTMLSession, UserAgent
import re,json

session = HTMLSession()
h = session.get('https://movie.douban.com',
                headers={'User-Agent': UserAgent().random})
     
for item in h.html.xpath('//*[@id="reviews"]/div[2]/div'):
  print(item.find('.review-content')[0].text)
  print(re.findall('(.*?)... \(全文\)',item.find('.review-content')[0].text)[0])
