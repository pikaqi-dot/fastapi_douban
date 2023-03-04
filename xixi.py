from requests_html import HTMLSession,UserAgent
session=HTMLSession()
h=session.get('https://movie.douban.com/',headers={'User-Agent':UserAgent().random})
# h.html.render()
# with open('测试.html','w') as f:
#     f.write(str(h.html.html))
for item in h.html.xpath('//*[@class="screening-bd"]//*[@class="ui-slide-item"]')[:-2]:
    print(item.find('.title>a',first=True).text)
