import nntplib
from urllib.request import urlopen
import textwrap
import re
from email.header import decode_header
import chardet
import base64
import configparser
import webbrowser
import time
import os

# 读取文件获得服务器地址
def getAddress():
    config = configparser.ConfigParser()
    config.read('config.ini')
    nntps = []
    for value in config.items('serverAddress'):
        nntps.append(value[1])
    return nntps

# 添加新的服务器地址
def addNewAddress(newAddress, nntps):
    count = len(nntps)
    nntps.append(newAddress)
    with open('config.ini', 'a', encoding='utf-8') as configFile:
        configFile.write(f"web{count+1} = {newAddress}\n")


def DeleteAddress(Num, nntps):
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    # 读取 config.ini 文件
    config.read('config.ini')
    # 指定要删除选项的节名称和选项名称
    section = 'serverAddress'
    option_to_delete = 'Web{}'.format(Num)
    if config.has_section(section) and config.has_option(section, option_to_delete):
        config.remove_option(section, option_to_delete)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    nntps.pop(Num - 1)


def is_base64(str):
    if ':' in str:
        return False
    else:
        return True

def coding(str):
    if is_base64(str):
        decoded_bytes = base64.b64decode(str)
        decoded_string = decoded_bytes.decode('UTF-8', errors = 'replace')
        return decoded_string
    else:
        return str


class NewsAgent:
    """
    可将新闻源中的新闻分发到新闻目的地的对象
    """

    def __init__(self):
        self.sources = []
        self.destinations = []
    
    def add_source(self, source):
        self.sources.append(source)
    
    def addDestiantion(self, Dest):
        self.destinations.append(Dest)

    def distribute(self):
        """
        从所有新闻源获取所有的新闻，并将其分发到所有的新闻目的地
        """
        items = []
        for source in self.sources:
            items.extend(source.get_items())
        for dest in self.destinations:
            dest.receive_items(items)


class NewsItem:
    """
    由标题和正文组成的简单新闻
    """
    def __init__(self, title, body):
        self.title = title
        self.body = body

class NNTPSource:
    """
    从NNTP新闻源获取新闻的类
    """
    def __init__(self, servername, group, howmany):
        self.servername = servername
        self.group = group
        self.howmany = howmany
    
    def get_items(self):
        server = nntplib.NNTP(self.servername)
        resp, count, first, last, name = server.group(self.group)
        start = last - self.howmany + 1
        resp, overviews = server.over((start, last))
        for id, over in overviews:
            title = decode_header(over['subject'])
            resp, info = server.body(id)
            body = '\n'.join(line.decode('latin')
                             for line in info.lines) + '\n\n'
            yield NewsItem(title, body)
        server.quit()

class SimpleWebSource:
    """
    使用正则表达式从网页提取新闻的新闻源
    """

    def __init__(self, url, title_pattern, body_pattern, encoding = 'utf-8'):
        self.url = url
        self.title_pattern = re.compile(title_pattern)
        self.body_pattern = re.compile(body_pattern)
        self.encoding = encoding
    
    def get_items(self):
        raw_data = urlopen(self.url).read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        text = raw_data.decode(encoding)
        titles = self.title_pattern.findall(text)
        bodies = self.body_pattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, textwrap.fill(body) + '\n')

class PlainDestination:
    """
    以纯文本方式显示所有新闻的新闻目的地
    """
    def receive_items(self, items):
        for item in items:
            print(item.title)
            print('-' * len(item.title))
            print(item.body)

class HTMLDestination:
    """
    以HTML格式显示所有新闻的新闻目的地
    """

    def __init__(self, filename):
        self.filename = filename
    
    def receive_items(self, items):

        out = open(self.filename, 'w',  encoding = 'utf-8', errors = 'replace')
        print("""
        <html>
          <head>
            <title>Today's News</title>
          </head>
          <body>
          <h1>Today's News</h1>
        """, file = out)

        print('<ul>', file = out)
        id = 0
        for item in items:
            id +=1
            print(' <li><a href="#{}">{}</a></li>'
                  .format(id, item.title), file = out)
        print('</ul>', file = out)

        id = 0
        for item in items:
            id += 1
            print('<h2><a name="{}">{}</a></h2>'
                  .format(id, item.title), file = out)
            print('<pre>{}</pre>'.format(coding(item.body)), file = out)

        print("""
          </body>
        </html>
        """, file = out)

def runDefaultSetup(servername, groupName):
    """
    默认的新闻源和目的地设施，根据偏好修改
    """

    agent = NewsAgent()

    # 从人民网获取新闻的SimpleWebSource对象：
    people_url = 'http://www.people.com.cn'
    people_title = r'<h2><a href="[^"]*"\s*>(.*?)</a>'
    people_body = r'</h2><p>(.*?)</p>'
    people = SimpleWebSource(people_url, people_title, people_body)

    agent.add_source(people)

    # 从comp.lang.python.announce获取新闻的NNTPSource对象：
    clpa_server = servername
    # comp.lang.python.announce
    clpa_group = groupName
    clpa_howmany = 10
    clpa = NNTPSource(clpa_server, clpa_group, clpa_howmany)
    fileName = 'news({}).html'.format(clpa_server.replace('.', '-'))

    agent.add_source(clpa)

    # 添加纯文本目的地和HTML目的地：
    agent.addDestiantion(PlainDestination())
    agent.addDestiantion(HTMLDestination(fileName))

    # 分发新闻
    agent.distribute()

    #展示新闻
    time.sleep(3)
    current_dir = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_dir, fileName)
    file_url = 'file://' + file_path
    webbrowser.open(file_url)


if __name__ == '__main__':
    runDefaultSetup('freenews.netfront.net', 'comp.lang.python.announce')

















