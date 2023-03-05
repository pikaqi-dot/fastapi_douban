from requests_html import HTMLSession, UserAgent
import re,json

session = HTMLSession()
h = session.get('https://movie.douban.com/subject/10876425/?from=playing_poster',
                headers={'User-Agent': UserAgent().random})
     
print(

    re.findall("制片国家/地区: (.*?)',",str( h.html.find('.article #info')[0].text.split('\n')))
  
 )
