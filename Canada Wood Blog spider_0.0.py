#!/usr/bin/env python
# encoding: utf-8
import time
import requests
import bs4
from bs4 import BeautifulSoup
import random
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

file_name = 'C:/Users/James/Desktop/canada_wood_blog_list.txt'
file_content = ''  # content to be written
file_content += 'update time：' + time.asctime()

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]


def wood_blog_spider(blog_tag):
    global file_content, headers    #, soup_content

    url = "https://canadawood.org/blog/%s/"  % blog_tag
    source_code = requests.get(url, headers=random.choice(headers))
    # just get the code, no headers or anything
    plain_text = source_code.text
    # BeautifulSoup objects can be sorted through easy
    soup = BeautifulSoup(plain_text)



    title_divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    # %t is space
    file_content += title_divide + '\t' * 4 + \
        blog_tag + '：' + title_divide
    count = 0

    for blog_info in soup.findAll('article'):
      if isinstance(blog_info, bs4.element.Tag):  # If item under tag "article" is not none
        count += 1
        print ('tag: %s, count: %d\n' % (blog_tag, count))

        if isinstance(blog_info.find('h3', {'class': 'entry-title'}), bs4.element.Tag):
          title = blog_info.find('h3', {'class': 'entry-title'}).string.strip()
          print('title: %s\n' % (title))
          file_content += "*%d\t《%s》\n\n" % (count, title)
        else:
          print ("Miss of title\n\n")

        if isinstance(blog_info.find_next_sibling('p'), bs4.element.Tag):
          abst = blog_info.find_next_sibling('p')
          print('abstract: %s\n' % (abst.get_text().rstrip('more')))
          file_content += "abstract：\n%s\n\n" % (abst.get_text().rstrip('more'))
        else:
          print ("Miss of abstract\n\n")

      else:
        print ("There is no article under tag %s\n\n"  %  blog_tag)




def do_spider(blog_lists):
    for blog_tag in blog_lists:
        wood_blog_spider(blog_tag)


#The code under "if __name__ == 'main':"  will only be excute when this file is excuted directely as script, rather than import to other script
# "if __name__ == 'main':" 下的代码只有在文件作为脚本直接执行时才会被执行，而import到其他脚本中是不会被执行的。
if __name__ == "__main__":
    blog_lists = ['china', 'korea', 'japan', 'india', 'canada', 'uk-europe']
    do_spider(blog_lists)

    # write result to file
    f = open(file_name, 'w',encoding='utf-8')
    f.write(file_content)
    f.close()



