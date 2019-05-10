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
    need_divs = []
    for each in all_divs:
        if "相关链接" in each.text:
            div_len += 1
            j1 = 1
            need_divs.append(each)
        if "友情链接" in each.text:
            div_len += 1
            j1 =2
            need_divs.append(each)
        #     print('*'*100)
        #     print(each)
        #     print('*' * 10)
        #     print(each.text.strip())
        #     print(each)
    print("相关div有%s层" % div_len)
    # 当相关div数量大于3个的时候，选择text第三层的div进行爬取
    if j1 != 0:
        if div_len >= 3:
            a_div = need_divs[2]
            link_text = a_div.text
            print(link_text)
        else:
            a_div = need_divs[-1]
            link_text = a_div.text
            print(link_text)
    else:
        link_text = ''
    # j1代表相关链接or友情链接；a_div为内容
    return j1,link_text

    # except:
    #     print("URL解析错误")
# # 存入csv
# def save_csv():
#     mkpath = os.getcwd()
#     adds = '链接数据test'
#     path = mkpath + '/' + adds + '.csv'
#     csvfile = open(path, 'a+', encoding='utf-8', newline='')
#     writer = csv.writer(csvfile)
#     writer.writerow(('网站编号', '网站名称', '网站url', '网站链接情况','链接内容'))
#     return writer

# 存入xls
def save_xls():
    mkpath = os.getcwd()
    link_path = mkpath + '/链接test.xls'
    link_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    link_sheet = link_book.add_sheet('test', cell_overwrite_ok=True)
    i = 0
    titles = ['网站序号', '网站名称', '网站url', '网站链接情况','链接内容']
    for title in titles:
        link_sheet.write(0, i, title)
        i += 1
    return link_sheet,link_path,link_book

# 从base_list中遍历初始官媒的URL和名称
def get_url():
    urls = base_list.all_urls
    webnames =base_list.all_webname
    # 创建xls
    (link_sheet,link_path,link_book) = save_xls()
    for i in range(1,len(urls)):
        url = urls[i]
        webname = webnames[i]
        print("正在爬取“%s”的相关链接" % webname)
        # 解析URL获取链接
        (j1,link_text)=main_url(url)
        print('*' * 100)
        # 存入xls
        if j1 == 0:
            link_state = "无"
        elif j1 == 1:
            link_state = "友情链接"
        else:
            link_state = "相关链接"
        link_sheet.write(i, 0, i)
        link_sheet.write(i, 1, webname)
        link_sheet.write(i, 2, url)
        link_sheet.write(i, 3, link_state)
        link_sheet.write(i, 4, link_text)
        time.sleep(1)
    link_book.save(link_path)

get_url()