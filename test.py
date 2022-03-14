# -*- coding:utf-8 -*-
# @Time    : 2022/3/10 19:34
# @Author  : Yinkai Yang
# @FileName: test.py
# @Software: PyCharm
# @Description: this is a program related to get detailed information about teachers
import requests
from bs4 import BeautifulSoup

teacher = []
proxy = []
header = []


# 暂时还没有用上
def preparation():
    # 创建一些proxy、header，随机选取防止被拉黑
    proxy = [
        {'proxy': 'https://183.166.162.182:9999'},
        {'proxy': 'https://112.111.217.76:9999'},
        {'proxy': 'https://114.239.150.98:9999'},
        {'proxy': 'https://115.218.7.204:9000'}
    ]
    header = [
        {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
        {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'},
        {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
        {'user-agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'},
        {
            'user-agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)'},
        {
            'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'},
        {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)'},
        {
            'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)'}
    ]
    return


def read_file():
    with open('teacher.txt', 'r') as f:
        list_tmp = []
        lines = f.readlines()

        for i in lines:
            list_tmp.append(i.rstrip('\n'))
            teacher.append(i.rstrip('\n'))
        f.close()
        # print(list_tmp)
        return list_tmp


def get_data(url):
    # 获取页面的内容，然后进行soup操作
    page = requests.get(url=url)
    content = page.text

    # debug
    # print(content)

    # 创建soup
    soup = BeautifulSoup(content, 'html.parser')

    return soup


def soup_easy(soup):
    # 通过soup进行操作，这里才是操作的关键
    for item in soup.find('li', attrs={'itemtype': 'http://schema.org/Person'}):
        # print(item)  # 获得预期的标签结果
        # 获得a标签里面的链接，写进list
        thing = " "
        thing = item.select('a')
        # print(thing)
        print(thing[0].get('href'))

    return thing[0].get('href')


def soup_difficult(soup):
    journal = []
    counter = 0  # 计数器

    # 核心查询部分find_all
    for item in soup.find_all('cite', attrs={'class': 'data tts-content'}):
        # 控制打印，便于debug
        # print(item.get_text().encode('utf-8'))
        journal.append(item.get_text().encode('utf-8'))

        counter = counter + 1
    print(counter)  # 可以不打印输出
    return journal


def write_file(journal,count):
    # 批量创建对应老师的txt文件
    full_path = teacher[count] + '.txt'
    with open(full_path, 'w+', encoding='utf-8') as f:
        for i in journal:
            # gbk和utf-8之间的冲突，利用replace进行解决
            f.write(i.decode('utf-8'))
            f.write('\n')
    f.close()
    return


def main():
    # 将数据读入list中，通过循环进行循环操作，一口气将所有数据一口气得到

    # 测试用例
    # url = 'https://dblp.uni-trier.de/search?q=' + 'Guilin%20Qi'
    # url = 'https://dblp.uni-trier.de/search?q=' + 'Guilin_Qi'

    count = 0  # 计数器
    link_list = read_file()
    for i in link_list:
        url = 'https://dblp.uni-trier.de/search?q=' + i
        # 第一次进行链接的访问
        soup = get_data(url)
        link_url = soup_easy(soup)

        # 第二次进入核心链接进行访问
        link_soup = get_data(link_url)
        write_file(soup_difficult(link_soup),count)
        # 计数器加1
        count = count + 1

    return


if __name__ == '__main__':
    main()
