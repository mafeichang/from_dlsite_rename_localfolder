# -*- encoding: utf-8 -*-
#!\usr\bin\env python
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


def main():
    for d in dirs:
        try:
            match_rj = rj_re.search(d).group()
            img_re = re.compile(r'img')
            d_filelist = os.listdir(d)
            re_result = []
            for file_name in d_filelist:
                img_search = img_re.findall(file_name)
                re_result = re_result + img_search
            if len(re_result) > 0:
                print('%s img is exist' % match_rj)
                continue
            else:
                dl_url = 'http://www.dlsite.com/maniax/work/=/product_id/' + str(match_rj) + '.html'  # 每个文件夹RJ号的网站链接
                r = requests.get(dl_url, headers=headers, proxies=proxies)
                file_content = r.text
                tree = etree.HTML(file_content)  # 对html文本使用 etree.HTML(html)解析,得到Element对象
                # 下载图片并以RJ号保存文件名
                img_xpath = tree.xpath('//div[@class="product-slider-data"]/div/@data-src')
                for img_search in img_xpath:
                    imgurl = 'http:' + img_search
                    imgname_re = re.compile(r'[\w.]*\.jpg')  # 正则表达式表达jpg文件名
                    imgname = imgname_re.search(img_search).group()  # 正则匹配jpg文件名
                    response = requests.get(imgurl, headers=headers, proxies=proxies)  # get 图像
                    imgpath = os.path.join(d, imgname)  # 本地img路径
                    try:
                        with open(imgpath, 'wb') as f:
                            f.write(response.content)
                            print("Downloaded " + imgname)
                    except IOError as e:
                        with open(d + 'imgerror.txt', 'a') as f:
                            f.write(e + '\n%s download error\n\n' % imgname)
                        print("%s Img saved failed" % d)
        except TimeoutError as e:
            print(d + '\n网络请求超时:%s\n\n' % e)
        except Exception as e:
            print(d + '\n重命名失败，原因：\n %s\n\n' % e)
    input('Press Enter to exit...')


if __name__ == '__main__':
    main()
