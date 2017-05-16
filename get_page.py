from bs4 import BeautifulSoup
import urllib
import re

"""cuts a string at the next dot after the amount"""
def soft_cut_string(string,amount):
    if len(string) > amount:
        nextDotIndex = string.find(".",amount,-1)
        return string[:nextDotIndex+1]
    else:
        return string

"""returns a dict containing a page title, url and all the text from the <p>'s in the page"""
def get_rand_wiki_page():
    page = urllib.request.urlopen('http://en.wikipedia.org/wiki/Special:Random')
    dom = BeautifulSoup(page.read(), 'html.parser')

    url = page.geturl()
    title = dom.find(id='firstHeading').string

    paragraphs = dom.find_all('p')
    text = ''
    for p in paragraphs:
        text+=p.get_text()+'\n'
    #remove references in wikipage
    text = re.sub(r"\[\d+\]","",text)
    page.close()

    return {'title':title,'url':url,'text':text}