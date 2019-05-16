# -*- coding: utf-8 -*-

from url_link import url_link
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


# # 查找所有class属性为hd的div标签
# div_list = soup.find_all('div', class_='hd')
# # 查找所有class属性为hd的div标签下的a标签的第一个span标签
# div_list = soup.select('div.hd > a > span:nth-of-type(1)')
# # 查找所有class属性为hd的div标签下的a标签的第一个span标签
# urls = et_html.xpath("//div[@class='hd']/a/span[1]")

# 根据URL定位div获取link的url
# 存入xls
def save_xls():
    mkpath = os.getcwd()
    link_path = mkpath + '/链接test.xls'
    link_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    link_sheet = link_book.add_sheet('test', cell_overwrite_ok=True)
    i = 0
    titles = ['网站编号', '网站名称', '网站url', '网站层级', '网站链接情况', '链接数量', '链接名称', '链接URL', '链接真名']
    for title in titles:
        link_sheet.write(0, i, title)
        i += 1
    return link_sheet, link_path, link_book
# 存入csv
def save_csv():
    mkpath = os.getcwd()
    path = mkpath + '/链接test.csv'
    csvfile = open(path, 'a+', encoding='utf-8', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(('网站编号', '网站名称', '网站url', '网站层级', '网站链接情况', '链接数量', '链接名称', '链接URL', '链接真名'))

    count_path = mkpath + '/(count)链接test.csv'
    csvfile = open(count_path, 'a+', encoding='utf-8', newline='')
    count_writer = csv.writer(csvfile)
    count_writer.writerow(('网站编号', '网站名称', '网站url'))
    return writer, count_writer

# 传入URL列表，调用函数获取子link，保存数据，返回2层的URL列表
def get_url(urls, webnames, linkrank, linkid, all_urls):
    b_urls = []
    b_webnames = []
    b_ranks = []
    # 遍历获取urls中的url，单个url爬取
    for i in range(0, len(urls)):
        url = urls[i]
        webname = webnames[i]
        # linkid为链接的系统编号，唯一标识
        linkid += 1
        # s_rank为链接的层级编号，如0-1-11-12，即第一层的1链接的11子链接的12子链接,linkrank为父链接的层级编号
        s_rank = str(linkrank)+'--'+str(i+1)
        # 写入链接count表
        count_writer.writerow((linkid, webname, url))
        print("正在爬取“%s”的子链接，系统编号为%s，层级编号为%s" % (webname, linkid, s_rank))
        # 调用url_link，解析URL获取link
        # 判断之前未爬取，继续爬取，如果已经爬取，则跳过
        if url not in all_urls:
            (j1, link_names, link_urls, link_names_real) = url_link(url)
            # 将成功爬取的url加入到all_urls，去重防止再爬
            all_urls.append(url)
        else:
            print('*' * 20, "该链接已经爬取过，跳过重复爬取", '*' * 20)
            j1 = 3
            link_names = []
            link_urls = []
        # 判断链接状态
        if j1 == 0:
            link_state = "无"
        elif j1 == 1:
            link_state = "有"
        elif j1 == 2:
            link_state = "无法获取"
        elif j1 == 3:
            link_state = "已爬取"
        elif j1 == 4:
            link_state = "有（注释）"
        # 存入xls，只能最后存入
        link_sheet.write(linkid, 0, linkid)
        link_sheet.write(linkid, 1, webname)
        link_sheet.write(linkid, 2, url)
        link_sheet.write(linkid, 3, s_rank)
        link_sheet.write(linkid, 4, link_state)
        link_sheet.write(linkid, 5, len(link_urls))
        link_sheet.write(linkid, 6, link_names)
        link_sheet.write(linkid, 7, link_urls)
        link_sheet.write(linkid, 8, '')
        # 存入csv，可同步存入
        writer.writerow((linkid, webname, url, s_rank, link_state, len(link_urls), link_names, link_urls, ''))
        time.sleep(0.001)
        # 判断urls是否为空，不为空的则传到下一级，作为下一次爬取链接的list, b_urls, b_webnames都是两层的list
        if link_urls != []:
            b_urls.append(link_urls)
            b_webnames.append(link_names)
            b_ranks.append(s_rank)

    print('*' * 20, "第%s层链接全部爬取完，存入xls，链接id已爬到：%s" % (linkrank,linkid), '*' * 20)
    print("链接list为", b_urls)
    return b_urls, b_webnames, linkid, b_ranks, all_urls

# 循环调用上一层的url列表，再次传入获取子链接URL
def loop_url(urls, webnames, linkrank, linkid, ir):
    all_urls = []
    while 1:
        if ir == 2:
            print("爬取完成")
            break
        else:
            print("*" * 100, "开始爬取%s子链接的子链接,层级为01" % linkrank, "*" * 100)
            # 此处的urls为0层的原始list，返回的urls_1为0-X的2层子链接list
            (urls_1, webnames_1, linkid, ranks_1, all_urls) = get_url(urls, webnames, linkrank, linkid, all_urls)
            for i1 in range(0, len(urls_1)):
                print("*" * 100, "正在爬取%s的子链接,层级为02" % linkrank, "*" * 100)
                print("0-%s中X=" % i1, len(urls_1))
                urls = urls_1[i1]
                webnames = webnames_1[i1]
                linkrank = ranks_1[i1]
                # 此处urls为0-X的子链接list，返回的urls_2为0-X-X的2层子链接list
                (urls_2, webnames_2, linkid, ranks_2, all_urls) = get_url(urls, webnames, linkrank, linkid, all_urls)
                # for i2 in range(0, len(urls_2)):
                #     print("*" * 100, "正在爬取%s的子链接,层级为03" % linkrank, "*" * 100)
                #     print("0-%s-X中的X" % i2, len(urls_2))
                #     urls = urls_2[i2]    #此处urls为0-X-X的子链接list
                #     webnames = webnames_2[i2]
                #     linkrank = ranks_2[i2]
                #     # 此处urls为0-x-x的2层子链list
                #     (urls_3, webnames_3, linkid, ranks_3, all_urls) = get_url(urls, webnames, linkrank, linkid, all_urls)
                #     for i3 in range(0, len(urls_3)):
                #         print("*" * 100, "正在爬取%s的子链接,层级为04" % linkrank, "*" * 100)
                #         print("0-X-%s-x中的X" % i3, len(urls_3))
                #         try:
                #             urls = urls_3[i3]  # 此处urls为0-X-X的子链接list
                #             webnames = webnames_3[i3]
                #             linkrank = ranks_3[i3]
                #             # 此处urls为0-x-x的2层子链list
                #             (urls_4, webnames_4, linkid, ranks_4, all_urls) = get_url(urls, webnames, linkrank, linkid, all_urls)
                #         except:
                #             print("爬取失败")
            print("*" * 100, "所有链接爬取成功！！！", "*" * 100)
            ir += 1

# # 递归函数
# def all_main(urls, webnames, linkrank, linkid, ir):
#     # linkrank为层级编号,linkid为唯一编号
#     (b_urls, b_webnames, linkid, b_ranks) = get_url(urls, webnames, linkrank, linkid)
#     aid = linkid
#     linkid = aid
#     # ir为层级，设定三层后停止
#     ir += 1
#     if ir == 3:
#         print("爬取完成")
#     else:
#         for i in range(0, len(b_urls)):
#             urls = b_urls[i]
#             webnames = b_webnames[i]
#             linkrank = b_ranks[i]
#             print("*" * 100, "正在爬取%s的子链接,层级为%s" % (linkrank, ir))
#             all_main(urls, webnames, linkrank, linkid, ir)
#             print("*" * 100, "%s的子链接爬取成功" % linkrank)

# 从base_list中遍历初始官媒的URL和名称

# 赋值
# urls为每次传入爬取的父链接list；
# linkrank为待爬取urls的父链接的层级编号，如0-1-1-1
# linkid为带爬取的url的唯一系统编号
# webnames为urls对应的网站名称
# all_urls为所有urls的list，重要作用是去重，避免重复爬取3

linkrank = 0
linkid = 0
ir = 1
urls = base_list.all_urls
webnames = base_list.all_webname


# 创建xls和csv
(link_sheet, link_path, link_book) = save_xls()
(writer, count_writer) = save_csv()

# 递归函数，已放弃
# all_main(urls, webnames, linkrank, linkid, ir)
# 多层循环函数传入URL的list
loop_url(urls, webnames, linkrank, linkid, ir)

# 保存xls，并关闭
link_book.save(link_path)