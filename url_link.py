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

# 根据URL获取子链接的网页名称
def get_linkname(url):
    link_name_real = ''
    try:
        # 通过url获取网页内容，返回r
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        file = urllib.request.urlopen(req, timeout=5)
        r = file.read()
        soup = BeautifulSoup(r, 'html5lib')
        titles = soup.find_all('title')
        for title in titles:
            link_name_real = title.get_text()
    except:
        print("无法获取URL本页面的网站名称")
    return link_name_real



# 根据URL定位div获取link的url
def url_link(url):
    try:
        # 通过url获取网页内容，返回r
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        file = urllib.request.urlopen(req, timeout=5)
        r = file.read()
        soup = BeautifulSoup(r, 'html5lib')

        # 遍历所有div，定位友情链接所在div，将相关div添加到list中，判断list长度，选取合适的div爬取友情链接
        all_divs = soup.find_all('div')
        div_len = 0
        j1 = 0
        need_divs = []
        for each_div in all_divs:
            if "友情链接" in each_div.text or "相关链接"in each_div.text or "相关网站"in each_div.text or "合作媒体"in each_div.text:
                div_len += 1
                j1 = 1
                need_divs.append(each_div)
        print("相关div有%s层" % div_len)

        link_names = []
        link_names_real = []
        link_urls = []
        url_self = ''.join(re.findall(r"\.(.+?)\.", url))
        # 当存在子链接时候进行爬取，否则返回无
        if j1 == 1:
            a_div = need_divs[-1]
            div_as = a_div.find_all('a')
            if len(div_as) >= 2:
                print("爬取div[-1]")
            else:
                # 当相关div数量大于3个的时候，选择[-2]层的div进行爬取
                a_div = need_divs[-2]
                div_as = a_div.find_all('a')
                print("爬取div[-2]")
            # 遍历div中所有的a标签
            for div_a in div_as:
                # 获取a标签中的text，默认为子链接的名称，正则也可以获取
                r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
                link_name = re.sub(r1, '', str(div_a.get_text()))
                link_url = div_a.get('href')
                # 获取a标签中的href，默认为子链接的URL，判断非空继续
                if link_url != '':
                    # 判断为html链接，继续
                    if "http" in link_url:
                        # 判断为非图片链接，继续
                        if "//img." not in link_url:
                            # 判断为非本站链接，继续
                            if url_self not in link_url:
                                # 判断子链接没有重复爬取，去重，继续
                                if link_url not in link_urls:
                                    # 父链接网站中的子链接网站名称并不一定正确，直接爬取原网站的名称
                                    # 判断子链接名称非空值，继续
                                    if link_name != '' and len(link_name) <= 15:
                                        # link_name_real = get_linkname(url)
                                        link_name_real = '测试'
                                        link_names.append(link_name)
                                        link_urls.append(link_url)
                                        link_names_real.append(link_name_real)

            print("获取子链接数量为：", len(link_urls))
        else:
            print("没有相关链接")
        # j1代表相关链接or友情链接；link_names为子链接名称；link_urls为子链接地址
        return j1, link_names, link_urls, link_names_real

    except:
        print("URL解析错误")
        return 2, [], [], []
