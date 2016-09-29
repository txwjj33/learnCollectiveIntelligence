# _*_ coding: UTF-8 _*_
'''
作用：电影推荐函数
时间：2016-9-29
备注: 各个csv文件的数据格式
links.csv:    movieId | imdbId  | tmdbId
movies.csv:   movieId | title   | genres(such as Adventure|Animation|Children|Comedy|Fantasy)
ratings.csv:  userId  | movieId | rating | timestamp
tags.csv:     userId  | movieId | tag    | timestamp
各个数据格式
'''

import csv
import os, os.path
import time

import functions
import recommendation

osjoin = os.path.join

dataset_dir = osjoin("..", "dataset", "ml-latest-small")

def test_sqlite():
    import sqlite3

    conn = sqlite3.connect(osjoin(dataset_dir, "test.db"))
    cur = conn.cursor()
    # 创建表
    create_table = "create table books (title, author, lang)"
    cur.execute(create_table)

    # 插入数据
    cur.execute('insert into books values ("test_title", "txw", "python")')
    # 读取
    cur.execute('select * from books')
    print(cur.fetchall())

    conn.commit()
    cur.close()
    conn.close()

# 读取评分数据
def get_ratings_csv():
    with open(osjoin(dataset_dir, "ratings.csv"), "rb") as file_csv:
        spamreader = csv.reader(file_csv)
        result = {}
        k = 0
        for row in spamreader:
            k += 1
            if k == 1: continue
            userId = int(row[0])
            result.setdefault(userId, {})
            movieId = int(row[1])
            result[userId][movieId] = float(row[2])

    return result

#读取电影名字数据
def get_title_csv():
    with open(osjoin(dataset_dir, "movies.csv"), "rb") as file_csv:
        spamreader = csv.reader(file_csv)
        result = {}
        k = 0
        for row in spamreader:
            k += 1
            if k == 1: continue
            result[int(row[0])] = row[1]

    return result

# 计算电影相似度
def calculate_similar_items():
    ratings = get_ratings_csv()
    result = recommendation.calculate_similar_items(ratings)
    functions.output_to_json(result, osjoin(dataset_dir, "similar.json"))

# 计算某个用户的推荐
def get_recommendations(userId, n = 100):
    ratings = get_ratings_csv()
    recommendations = recommendation.get_recommendations(ratings, userId)
    print recommendations[0:n]

# 输出某个用户的推荐电影名字
def print_recommendations_with_title(userId, n = 100):
    ratings = get_ratings_csv()
    titles = get_title_csv()
    recommendations = recommendation.get_recommendations(ratings, userId)
    for k in xrange(1, min(n, len(recommendations))):
        r = recommendations[k]
        print r[0], titles[r[1]]

# 计算某个用户的推荐(使用电影相似度)
def get_recommendations_by_item(userId):
    result = get_ratings()
    matches = recommendation.get_recommendations(result, userId)
    print matches[0:100]

if __name__ == '__main__':
    calculate_similar_items()

