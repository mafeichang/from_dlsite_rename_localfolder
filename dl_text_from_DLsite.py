# -*- encoding: utf-8 -*-
import re
import requests
import os
from lxml import etree

input_path = u'.' #所有文件夹
dirs = [f for f in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, f))] #遍历本地文件夹
rj_re = re.compile(r'RJ\d*')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
           'AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/56.0.2924.87 Safari/537.36'}
proxies = {'http': "socks5://127.0.0.1:1080", 'https': "socks5://127.0.0.1:1080"}

for d in dirs:
    if os.path.isfile(os.path.join(d, 'DLsite作品内容紹介.txt')):
        print('%s DLsite作品内容紹介已经存在' % d)
        continue
    else:
        try:
            # 获取作品页面源代码
            match_rj = rj_re.search(d).group()
            dlurl = 'http://www.dlsite.com/maniax/work/=/product_id/' + str(match_rj) + '.html'  # 每个文件夹RJ号的网站链接
            r = requests.get(dlurl, headers=headers, proxies=proxies)
            file_content = r.text
            tree = etree.HTML(file_content)  # 对html文本使用 etree.HTML(html)解析,得到Element对象
            # 下载作品内容文容
            text_xpath = tree.xpath('//div[@class="work_article work_story"]/text()')
            # print(text_xpath)
            textpath = os.path.join(d, "DLsite作品内容紹介.txt")
            txtfile = open(textpath, 'w', encoding='utf-8')
            try:
                for t in text_xpath:
                    text = t.strip("\r\n")
                    txtfile.write(text)
                    txtfile.write("\n")
                txtfile.close()
                print("Downloaded %s content" % match_rj)
            except:
                print("%s text saved failed" % d)
        except:
            print(os.path.join(input_path, d) + '\nSorry,could not found text for this folder\n')

input('Press Enter to exit...')
