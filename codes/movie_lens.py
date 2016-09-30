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

###############  解析数据相关函数
# 读取评分数据
def get_ratings_csv():
    with open(osjoin(dataset_dir, "ratings.csv"), "rb") as file_csv:
        spamreader = csv.reader(file_csv)
        result = {}
        k = 0
        for row in spamreader:
            k += 1
            if k == 1: continue
            user_id = int(row[0])
            result.setdefault(user_id, {})
            movie_id = int(row[1])
            result[user_id][movie_id] = float(row[2])

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
    file_name = osjoin(dataset_dir, "similar.db")
    recommendation.calculate_similar_items_save(ratings, file_name)


###############  电影相似度相关函数
# 查询某个电影的相似度列表
def get_similar(movie_id):
    file_name = osjoin(dataset_dir, "similar.db")
    return recommendation.get_similar_by_item(file_name, movie_id)

# 输出某个电影的相关电影的相似度和名字
def print_similar_with_title(movie_id):
    titles = get_title_csv()
    print "similar list of movie: " + titles[movie_id]
    file_name = osjoin(dataset_dir, "similar.db")
    result = recommendation.get_similar_by_item(file_name, movie_id)
    for (sim, movie) in result:
        print sim, movie, titles[movie]

# 计算某个用户的推荐(使用电影相似度)
# 由于sqlite查询时间过长，这个算法速度还比不上使用用户相似度算
def get_recommendations_by_item(user_id, n = 100):
    ratings = get_ratings_csv()
    file_name = osjoin(dataset_dir, "similar.db")
    recommendations = recommendation.get_recommendations_items_with_file(ratings, user_id, file_name)
    print recommendations[0 : n]


###############  用户相似度相关函数
# 计算某个用户的推荐
def get_recommendations(user_id, n = 100):
    ratings = get_ratings_csv()
    recommendations = recommendation.get_recommendations(ratings, user_id)
    print recommendations[0 : n]

# 输出某个用户的推荐电影名字
def print_recommendations_with_title(user_id, n = 100):
    ratings = get_ratings_csv()
    titles = get_title_csv()
    recommendations = recommendation.get_recommendations(ratings, user_id)
    for k in xrange(1, min(n, len(recommendations))):
        r = recommendations[k]
        print r[0], titles[r[1]]

if __name__ == '__main__':
    get_recommendations_by_item(1)
