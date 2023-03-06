from requests_html import HTMLSession, UserAgent
import re,json

session = HTMLSession()
h = session.get('http://39.101.79.110:8080/#/movie',
                headers={'User-Agent': UserAgent().random})
# h.html.render()
     
print(h.html.html)

