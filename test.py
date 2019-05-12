# -*- coding: utf-8 -*-

import base_list
import csv
import urllib
import re
from bs4 import BeautifulSoup
from lxml import html
import urllib.request
import html5lib
import time
import os
import xlwt

def main_url(url):
    # try:
    # 通过url获取网页内容，返回r
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    file = urllib.request.urlopen(req, timeout=5)
    r = file.read()
    soup = BeautifulSoup(r, 'html5lib')
    # # 能够获取所有文本，判断有无
    # tt = r.decode()
    # if "友情链接" in tt:
    #     print(1)
    # if "相关链接" in tt:
    #     print(2)
    # etree = html.etree
    # et_html = etree.HTML(r)

    # # 查找所有class属性为hd的div标签
    # div_list = soup.find_all('div', class_='hd')
    # # 查找所有class属性为hd的div标签下的a标签的第一个span标签
    # div_list = soup.select('div.hd > a > span:nth-of-type(1)')
    # # 查找所有class属性为hd的div标签下的a标签的第一个span标签
    # urls = et_html.xpath("//div[@class='hd']/a/span[1]")

    # 遍历所有div，定位友情链接所在div，将相关div添加到list中，判断list长度，选取合适的div爬取友情链接
    all_divs = soup.find_all('div')
    div_len = 0
    j1 = 0
    link_names = []
    link_urls = []
    for each in all_divs:
        if "相关链接" in each.text:
            div_len += 1
            j1 = 1
            div_a = each.find_all('a')
            print(div_a)
            link_names.append(each)
        if "友情链接" in each.text:
            div_len += 1
            j1 =2
            # 获取友情链接下的每一个a标签
            div_as = each.find_all('a')
            for div_a in div_as:
                print(div_a)
                r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
                link_name = re.sub(r1, '', ''.join(div_a))
                print(link_name)
                print(div_a['href'])
                link_names.append(link_name)
                link_urls.append(div_a['href'])
    print("相关div有%s层" % div_len)

url = 'http://www.people.com.cn'
main_url(url)