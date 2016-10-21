# _*_ coding: UTF-8 _*_

# 爬虫类
class crawler:
    def __init__(self, dbname):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

    # 用于获取条目的id，并且如果条目不存在，将其加入到数据库中
    def get_entry_id(self, table, field, value, create_new = True):
        return None

    # 为每个网页建立索引
    def add_to_index(self, url, soup):
        print "indexing %s" % url

    # 从一个html网页中提取文字（不带标签的）
    def get_text_only(self, soup):
        return None

    # 根据任何非空白字符进行分词处理
    def seperate_words(self, text):
        return None

    # 如果url已经建立索引，则返回true
    def isindexed(self, url):
        return False

    # 添加一个关联两个网页的连接
    def add_link_ref(self, url_from, url_to, link_text):
        pass

    # 从一小组网页开始进行广度优先搜索，直至某一给定深度
    # 期间为网页建立索引
    def crawl(self, pages, depth = 2):
        pass

    # 创建数据库表
    def create_index_tables(self):
        pass

