from requests_html import HTMLSession,UserAgent
session=HTMLSession()
h=session.get('https://movie.douban.com/subject/35043401/?from=showing',headers={'User-Agent':UserAgent().random})
# h.html.render()
# with open('测试.html','w') as f:
#     f.write(str(h.html.html))

print(h.html.xpath('//*[@id="info"]/span[3]'))