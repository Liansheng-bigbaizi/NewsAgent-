# NewsAgent-
NNTP新闻汇总
## 一、设计内容

### （一）功能设计

#### 服务器地址管理

实现对服务器地址的查询、添加与删除操作。用户可随时获取当前已配置的服务器地址列表，以便了解可用的新闻源。添加新地址功能允许用户扩展系统可获取新闻的来源，而删除功能则可用于清理不再使用或无效的服务器地址。
例如，在系统初始配置中可能包含一些常见的新闻服务器地址，用户若发现新的可靠新闻源，可通过添加功能将其纳入系统；若某个服务器停止服务或出现问题，可使用删除功能将其从列表中移除。

#### 新闻获取

支持从 NNTP 新闻源和网页两种渠道获取新闻。对于 NNTP 新闻源，用户可指定服务器地址和新闻组，系统将连接到相应的 NNTP 服务器，获取指定数量的新闻内容，包括标题和正文。从网页获取新闻时，利用正则表达式匹配网页中的新闻标题和正文模式，从指定的网页（如人民网）提取新闻信息。
如用户对特定领域的新闻感兴趣，可选择从相关的 NNTP 新闻组获取深度报道；同时，也能从大众新闻网站获取更广泛的新闻资讯，以满足不同用户的需求。
新闻分发与展示
将获取到的新闻分发到不同的目的地进行展示。提供纯文本和 HTML 两种展示格式，纯文本展示方式简单直接，适合在命令行环境或对格式要求不高的场景中快速浏览新闻标题和内容；HTML 格式则更适合在浏览器中查看，可通过超链接、标题分级等方式提供更好的阅读体验，方便用户查看新闻详情。

### （二）数据设计

#### 服务器地址存储

使用配置文件（```config.ini```）存储服务器地址。配置文件中的[serverAddress]节以键值对的形式记录服务器地址，键为自定义的标识符（如web1、web2等），值为服务器的实际地址。这种方式方便读取和修改服务器地址列表，同时便于系统维护和扩展。

#### 新闻数据结构

定义```NewItem```类来表示新闻项，包含title（标题）和body（正文）两个属性。在获取新闻过程中，无论是从 NNTP 新闻源还是网页，都将新闻信息封装成```NewItem```对象，以便在系统中统一处理和传递新闻数据。

### （三）界面设计

#### 命令行交互界面

设计简洁的命令行菜单，提供清晰的操作提示。用户通过输入数字选择相应的操作，如查询服务器地址、添加新地址、删除地址、获取新闻等。系统根据用户输入调用相应的功能模块，并在命令行中显示操作结果或提示信息，如成功添加服务器地址后的确认信息、获取新闻过程中的状态更新等。
## 二、设计工具

- ```configparser```：用于处理配置文件（```config.ini```），方便读取和写入服务器地址等配置信息，实现系统的可配置性。
- ```nntplib```：专门用于与 NNTP 服务器进行交互，实现从 NNTP 新闻源获取新闻的功能，遵循 NNTP 协议规范进行新闻的检索和下载。
- ```urllib.request```：用于从网页获取数据，在从网页提取新闻时，发送 HTTP 请求并获取网页内容，为后续的新闻提取提供数据基础。
- ```re```（正则表达式）：在从网页提取新闻时，通过编写正则表达式模式，精准匹配新闻标题和正文等内容，实现高效的网页新闻提取。
- ```email.header```：用于解码新闻标题等可能包含编码信息的内容，确保正确显示新闻标题，处理各种编码格式（如 Base64 编码等）。
- ```chardet```：用于检测网页数据的编码格式，自动识别网页内容的编码方式，以便正确解码网页内容，避免乱码问题。
- ```base64```：处理可能存在的 Base64 编码数据，如在新闻标题或正文中遇到 Base64 编码的内容时，进行解码操作。
- ```os```：用于操作系统相关的操作，如获取当前工作目录、拼接文件路径等，方便文件操作和系统资源管理。
- ```time```：在新闻分发后，通过短暂的延迟（```time.sleep```），生成HTML文件并打开浏览器查看。
- ```webbrowser```：用于在 HTML 新闻展示时，自动打开默认浏览器并加载生成的 HTML 文件，方便用户查看新闻内容，提供便捷的新闻阅读方式

## 三、设计步骤
### （一）需求分析与规划
明确系统的功能需求，包括服务器地址管理、新闻获取与分发展示等功能点。与潜在用户或相关人员沟通，了解他们对新闻来源、展示格式、操作便捷性等方面的期望和需求，确保系统功能能够满足实际使用场景。
根据需求确定系统的架构设计，规划各个功能模块之间的关系和交互方式，设计数据存储结构和界面布局，为后续的开发工作奠定基础。
### （二）模块设计与实现
#### 服务器地址管理模块
设计```getAddress```函数读取配置文件中的服务器地址列表，```addNewAddress```函数实现添加新地址并更新配置文件，```DeleteAddress```函数用于删除指定地址并同步修改配置文件。对这些函数进行详细的代码实现，确保服务器地址管理操作的准确性和稳定性。
#### 新闻源模块
开发```NNTPSource```类，实现从 NNTP 新闻源获取新闻的功能。在类中实现```get_items```方法，通过nntplib连接服务器、获取新闻概述和详细内容，并封装成```Newstem```对象返回。同时，设计```SimpleWebSource```类，利用正则表达式从网页提取新闻，在```get_items```方法中实现网页数据获取、编码检测、正则匹配和新闻封装。
#### 新闻目的地模块
构建```PlainDestination```类，实现以纯文本方式展示新闻，在```receive_items```方法中遍历新闻列表并打印标题和正文。创建```HTMLDestination```类，在```receive_items```方法中生成 HTML 格式的新闻页面，包括标题、链接、正文等元素，并将其保存为 HTML 文件，最后使用```webbrowser```打开文件在浏览器中展示。
#### 新闻代理模块
设计```NewsAgent```类作为新闻获取和分发的核心控制类。在类中维护新闻源和新闻目的地列表，通过```add_source```和```addDestination```方法添加相应对象，```distribute```方法实现从新闻源获取新闻并分发给所有目的地的功能。
### （三）界面整合与优化
在```init.py```中构建命令行交互界面，循环显示操作菜单，接收用户输入并调用相应的功能函数。优化菜单的显示格式，使其清晰易懂，同时对用户输入进行有效性验证，避免因错误输入导致程序异常。
        对系统整体进行测试，检查界面操作的流畅性和功能的正确性，根据测试结果对界面进行调整和优化，提高用户体验。

## 四、设计程序

### （一）服务器地址管理（```nntp.py```部分代码）
#### 1.获取服务器地址```getAddress```
```python
def getAddress():
    config = configparser.ConfigParser()
    config.read('config.ini')
    nntps = []
    for value in config.items('serverAddress'):
        nntps.append(value[1])
    return nntps
```
#### 2.添加服务器地址```addNewAddress```
```python
def addNewAddress(newAddress, nntps):
    count = len(nntps)
    nntps.append(newAddress)
    with open('config.ini', 'a', encoding='utf-8') as configFile:
        configFile.write(f"web{count+1} = {newAddress}")
```
#### 3.删除服务器地址```DeleteAddress```
```python
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
```
### （二）新闻源获取（```nntp.py```部分代码）
#### 1.NNTP新闻源类```NNTPSource```
```python
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
```
#### 2.网页新闻源类```SimpleWebSource```
```python
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
```
### （三）新闻目的地展示（```nntp.py```部分代码）
#### 1. 纯文本新闻目的地类```PlainDestination```
```python
class PlainDestination:
    """
    以纯文本方式显示所有新闻的新闻目的地
    """
    def receive_items(self, items):
        for item in items:
            print(item.title)
            print('-' * len(item.title))
            print(item.body)

```
#### 2. HTML 新闻目的地类```HTMLDestination```
```python
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
```
### （四）新闻代理与分发（```nntp.py```部分代码）
#### 1. 新闻代理类```NewsAgent```
```python
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
```
### （五）主程序与操作选择（```init.py```和```set.py```部分代码）
#### 1. 主程序```init.py```
```python
import set

if __name__ == '__main__':
    while True:
        print("""=====================================
                    1.获取当前所有的服务器地址
                    2.添加新的服务器地址
                    3.删除服务器地址
                    4.获取新闻
                    5.退出
        =====================================
        """)
        n = input("请输入对应操作前的序号：")
        set.Choice(n)
        if n == '5':
            break
```
#### 2. 操作选择函数```choice```（```set.py```）
```python
def Choice(n):
    nntps = nntp.getAddress()
    if n == '1':
        print("当前服务器列表")
        m = 1
        for i in nntps:
            print("{} : {}".format(m, i))
            m += 1

    elif n == '2':
        newAddress = input("请输入新的服务器地址:")
        nntp.addNewAddress(newAddress, nntps)

    elif n == '3':
        print("当前服务器列表")
        m = 1
        for i in nntps:
            print("{} : {}".format(m, i))
            m += 1
        Num = int(input("请输入要删除的服务器地址："))
        nntp.DeleteAddress(Num, nntps)


    elif n == '4':
        print("请选择服务器地址：")
        count = 1
        for i in nntps:
            print('{} : {}'.format(count, i))
            count += 1

        m = int(input())
        serverName = nntps[m - 1]
        groupName = input("请输入想要浏览的组：")
        try:
            nntp.runDefaultSetup(serverName, groupName)
        except Exception as e:
            print("An error exists:{}".format(e))

    elif n == '5':
        try:
            sys.exit()
        except SystemExit as e:
            print("退出成功：{}".format(e))

    else:
        print('请重新输入')
```
## 五、运行结果
### （一）服务器地址管理操作
#### 1. 获取服务器地址
选择操作 “1” 后，系统在命令行输出当前配置的服务器地址列表，格式清晰，每个地址前有对应的序号，方便用户查看和识别。例如：
```cmd
当前服务器列表
1 : freenews.netfront.net
2 : news.hkpcug.org
3 : ddt.demos.su
4 : fysh.org
5 : news.fysh.org
6 : news.man.lodz.pl
7 : news.thur.de
8 : news.uni-stuttgart.de
```
#### 2. 添加服务器地址
选择操作 “2”，输入新的服务器地址（如newserver.example.com）后，系统提示添加成功，并在下次获取服务器地址列表时显示新添加的地址。
```cmd
请输入新的服务器地址:newserver.example.com
```
#### 3. 删除服务器地址
选择操作 “3”，先显示服务器地址列表，用户输入要删除的地址序号（如 “3”），系统删除指定地址并更新列表，再次获取地址列表时该地址已不存在。
```cmd
当前服务器列表
1 : freenews.netfront.net
2 : news.hkpcug.org
3 : ddt.demos.su
4 : fysh.org
5 : news.fysh.org
6 : news.man.lodz.pl
7 : news.thur.de
8 : news.uni-stuttgart.de
9 : newserver.example.com
请输入要删除的服务器地址：9
```
### （二）新闻获取与分发操作
#### 1. 选择新闻源服务器和新闻组
选择操作 “4” 后，系统先列出服务器地址供用户选择，用户输入服务器序号（如 “1”），然后输入想要浏览的新闻组（如comp.lang.python.announce）。
```cmd
请选择服务器地址：
1 : freenews.netfront.net
2 : news.hkpcug.org
3 : ddt.demos.su
4 : fysh.org
5 : news.fysh.org
6 : news.man.lodz.pl
7 : news.thur.de
8 : news.uni-stuttgart.de
1
请输入想要浏览的组：comp.lang.python.announce
```
#### 2. 新闻获取与分发过程
系统根据用户选择从 NNTP 新闻源或网页获取新闻，在命令行显示获取新闻的进度信息，如 “正在从服务器获取新闻...”。获取完成后，根据用户配置的新闻目的地进行分发。
#### 3. 新闻展示
若选择纯文本展示，新闻标题和正文依次在命令行输出，标题以较醒目的方式显示（如加粗或加大字号），正文排版清晰。若选择 HTML 展示，系统自动打开默认浏览器，显示包含新闻标题、链接和正文的 HTML 页面，新闻标题可点击跳转到对应正文。
![image-20241123200454042](https://github.com/user-attachments/assets/ecad1bc4-1026-4aec-ad03-e42a3a98490d)
