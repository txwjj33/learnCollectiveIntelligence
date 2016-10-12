# _*_ coding: UTF-8 _*_
'''
作用：发现群组相关函数
时间：2016-9-27
备注: 第三章
'''
import os, os.path
import feedparser
import re

def get_words(html):
    # 去掉所有的html标记
    text = re.compile(r"<[^>]+>").sub("", html)
    # 利用非字母字符拆分出单词
    words = re.compile(r"[^A-Z^a-z]+").split(text)
    # 转成小写
    return [word.lower() for word in words if word != ""]

# 返回一个RSS订阅源的标题和包含单词计数的字典
def get_word_counts(url):
    doc = feedparser.parse(url)
    word_counts = {}
    # 遍历所有的文章
    for e in doc.entries:
        if "summary" in e:
            summary = e.summary
        else:
            summary = e.description

        words = get_words(e.title + " " + summary)
        for word in words:
            word_counts.setdefault(word, 0)
            word_counts[word] += 1

    return doc.feed.title, word_counts

def generate_feedvector():
    # 统计每个词出现的次数
    feed_count = {}
    word_counts = {}
    feed_list = [line for line in file("feedlist.txt")]
    for url in feed_list:
        title, wc = get_word_counts(url)
        word_counts[title] = wc
        for word, count in wc.items():
            feed_count.setdefault(word, 0)
            if count > 1: feed_count[word] += 1

    # 过滤掉常用的以及使用太少的词
    word_list = []
    for w, count in feed_count.items():
        frac = float(count) / float(len(feed_list))
        if frac > 0.1 and frac < 0.5:
            word_list.append(w)

    # 输出到文件
    out_name = os.path.join("..", "..", "dataset", "blogdata.txt")
    out = file(out_name, "w")
    out.write("Blog")
    for word in word_list:
        out.write("\t%s" % word)
    out.write("\n")
    for blog, wc in word_counts.items():
        out.write(blog)
        for word in word_list:
            if word in wc:
                out.write("\t%d" % wc[word])
            else:
                out.write("\t0")
        out.write("\n")

generate_feedvector()
