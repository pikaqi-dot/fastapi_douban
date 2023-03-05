from requests_html import HTMLSession, UserAgent
import re,json

session = HTMLSession()
h = session.get('https://movie.douban.com/subject/35043401/?from=showing',
                headers={'User-Agent': UserAgent().random})
# h.html.render()
# with open('测试.html','w') as f:
#     f.write(str(h.html.html))
k= list(
    map(lambda x: x.replace(":","':'"),
        h.html.find('.article #info')[0].text.split('\n')[:-2]))
print(

  str(k).replace('[','{').replace(']','}')
    
  
 )
