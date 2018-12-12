# -*- encoding: utf-8 -*-
import re
import requests
import os
import shutil
from lxml import etree

input_path = u'.'  # 所有文件夹
# input_path = r'F:\同人音声\未整理\rename folder\201808\!良品'
dirs = [f for f in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, f))]  # 遍历本地文件夹
rj_re = re.compile(r'RJ\d*')
renamed_re = re.compile(r'^\[.*\] ')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
           'AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/56.0.2924.87 Safari/537.36'}


def mv(i, o):
    if os.path.isdir(o):
        print(o)
    else:
        shutil.move(i, o)


def main():
    for d in dirs:
        check_renamed = re.findall(renamed_re, d)
        if check_renamed:
            print('%s\n该文件夹不需重命名\n\n' % d)
            continue
        else:
            try:
                match_rj = rj_re.search(d).group()
                dl_url = 'http://www.dlsite.com/maniax/work/=/product_id/' + str(match_rj) + '.html'  # 每个文件夹RJ号的网站链接
                proxies = {'http': "socks5://127.0.0.1:1080", 'https': "socks5://127.0.0.1:1080"}
                r = requests.get(dl_url, headers=headers, proxies=proxies)
                file_content = r.text  # 获取网页内容
                tree = etree.HTML(file_content)  # 对html文本使用 etree.HTML(html)解析,得到Element对象
                maker = tree.xpath('//*[@id="work_maker"]/tr/td/span/a/text()')[0]
                title = tree.xpath('//*[@id="work_name"]/a/text()')[-1]
                match_rj = rj_re.search(d).group()
                output_name = '[%s] %s %s' % (maker, title, match_rj)
                output_name = output_name.replace("\n", "")  # 不知道为何maker后面会有换行符，替换掉
                print(d + '\n重命名为：%s\n\n' % output_name)
                filtered_output_name = (''.join([i for i in output_name if i not in r"/\\:*?\"<>|"])).strip()
                mv(os.path.join(input_path, d), os.path.join(input_path, filtered_output_name))
            except Exception as e:
                print(d + '\nERROR：%s\n\n' % e)
    input('Press Enter to exit...')


if __name__ == '__main__':
    main()
