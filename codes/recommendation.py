# _*_ coding: UTF-8 _*_
'''
作用：推荐系统相关函数
时间：2016-9-27
备注
'''

import math
import time

# 利用距离计算相似度
# 一次遍历，性能稍微好点
def sim_distance(prefs, k1, k2):
    n, distance = 0, 0
    for item in prefs[k1]:
        if item in prefs[k2]:
            n += 1
            distance += math.pow(prefs[k1][item] - prefs[k2][item], 2)

    if n == 0:
        return 0
    else:
        return 1 / (1 + math.sqrt(distance))

def sim_distance_2(prefs, k1, k2):
    same_items = [item for item in prefs[k1] if item in prefs[k2]]
    if len(same_items) == 0: return 0
    distance = sum(pow(prefs[k1][item] - prefs[k2][item], 2) for item in same_items)
    return 1 / (1 + math.sqrt(distance))

def test_sim_distance():
    prefs = {}
    prefs["p1"] = {"m1": 3, "m2": 4}
    prefs["p2"] = {"m1": 4, "m3": 2}
    prefs["p3"] = {"m0": 2}
    print sim_distance(prefs, "p1", "p2")

# 皮尔逊相关性计算相似度
# 一次遍历，性能稍微好点
def sim_pearson(prefs, k1, k2):
    n, sum1, sum2, sum1_square, sum2_square, sum_product = 0, 0, 0, 0, 0, 0
    for item in prefs[k1]:
        if item in prefs[k2]:
            n += 1
            sum1 += prefs[k1][item]
            sum2 += prefs[k2][item]
            sum1_square += pow(prefs[k1][item], 2)
            sum2_square += pow(prefs[k2][item], 2)
            sum_product += prefs[k1][item] * prefs[k2][item]

    if n == 0:
        return -1
    else:
        num = sum_product - sum1 * sum2 / n
        den = math.sqrt((sum1_square - sum1 * sum1 / n) * (sum2_square - sum2 * sum2 / n))
        # !!!某一个的评分都相等时，den为0，返回1，不合理
        if den == 0: return 1
        result = num / den
        if result > 1: return 1
        if result < -1: return -1
        return result

def sim_pearson_2(prefs, k1, k2):
    same_items = [item for item in prefs[k1] if item in prefs[k2]]
    n = len(same_items)
    if n == 0: return -1

    sum1 = sum(prefs[k1][item] for item in same_items)
    sum2 = sum(prefs[k2][item] for item in same_items)
    sum1_square = sum(pow(prefs[k1][item], 2) for item in same_items)
    sum2_square = sum(pow(prefs[k2][item], 2) for item in same_items)
    sum_product = sum(prefs[k1][item] * prefs[k2][item] for item in same_items)

    num = sum_product - sum1 * sum2 / n
    den = math.sqrt((sum1_square - sum1 * sum1 / n) * (sum2_square - sum2 * sum2 / n))
    if den == 0: return 1  # ?
    return num / den

def test_sim_pearson():
    prefs = {}
    prefs["p1"] = {"m1": 3, "m2": 4, "m3": 2}
    prefs["p2"] = {"m1": 4, "m2": 2, "m4": 3}
    prefs["p3"] = {"m0": 2}
    print sim_pearson(prefs, "p1", "p2")

# 计算相似度最大的前几名
def top_matches(prefs, k, num = 5, sim = sim_distance):
    start_time = time.time()
    scores = [(sim(prefs, k, other), other) for other in prefs if other != k]
    scores.sort()
    scores.reverse()
    print "top_matches cost time %d" % (time.time() - start_time)
    return scores[0:num]

def test_top_matches():
    prefs = {}
    prefs["p1"] = {"m1": 3, "m2": 4, "m3": 2}
    prefs["p2"] = {"m1": 4, "m2": 2, "m4": 3}
    prefs["p3"] = {"m0": 2}
    prefs["p4"] = {"m0": 2, "m2": 3, "m3": 100}
    print top_matches(prefs, "p1")

# 使用所有其他k的相似度来计算某个k的推荐item排名
def get_recommendations(prefs, k, sim = sim_distance):
    start_time = time.time()
    scores = top_matches(prefs, k)
    totals = {}
    sim_sums = {}
    for other in prefs:
        if other == k: continue
        sim_num = sim(prefs, k, other)
        # 忽略相关性为负的情况
        if sim_num <= 0: continue
        for item in prefs[other]:
            # 已有的item忽略
            if item in prefs[k]: continue
            totals.setdefault(item, 0)
            totals[item] += prefs[other][item] * sim_num
            sim_sums.setdefault(item, 0)
            sim_sums[item] += sim_num

    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()

    print "get_recommendations cost time %d" % (time.time() - start_time)
    return rankings

def test_get_recommendations():
    prefs = {}
    prefs["p1"] = {"m1": 3, "m2": 4, "m3": 2}
    prefs["p2"] = {"m1": 4, "m2": 2, "m4": 3}
    prefs["p3"] = {"m0": 2}
    prefs["p4"] = {"m0": 2, "m2": 3, "m3": 100}
    print get_recommendations(prefs, "p1")

# 倒置矩阵，将人和评分对调
def transform_prefs(prefs):
    result = {}
    for k in prefs:
        for item in prefs[k]:
            result.setdefault(item, {})
            result[item][k] = prefs[k][item]
    return result

# 计算相近的物品
def calculate_similar_items(prefs, n = 10):
    start_time = time.time()
    result = {}
    prefs_item = transform_prefs(prefs)
    count = 0
    for item in prefs_item:
        count += 1
        if count % 100 == 0:
            print "%d / %d" %(count, len(prefs_item))
        scores = top_matches(prefs_item, item, n)
        result[item] = scores

    print "calculate_similar_items cost time %d" % (time.time() - start_time)
    return result

def test_calculate_similar_items():
    prefs = {}
    prefs["p1"] = {"m1": 3, "m2": 4, "m3": 2}
    prefs["p2"] = {"m1": 4, "m2": 2, "m4": 3}
    prefs["p3"] = {"m0": 2}
    prefs["p4"] = {"m0": 2, "m2": 3, "m3": 100}
    print calculate_similar_items(prefs)

# 使用计算好的相近物品列表来推荐
# item_match: 计算好的物品相似度列表
def get_recommendations_items(prefs, k, item_match):
    start_time = time.time()
    user_rankings = prefs[k]
    scores = {}
    total_sim = {}
    for (item, rating) in user_rankings.items():
        for (similarity, item2) in item_match[item]:
            if item2 in user_rankings: continue
            if similarity <= 0: continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity

    rankings = [(total / total_sim[item], item) for (item, total) in scores.items()]
    rankings.sort()
    rankings.reverse()

    print "get_recommendations_items cost time %d" % (time.time() - start_time)
    return rankings

def test_get_recommendations_items():
    prefs = {}
    prefs["p1"] = {"m1": 3, "m2": 4, "m3": 2}
    prefs["p2"] = {"m1": 4, "m2": 2, "m4": 3}
    prefs["p3"] = {"m0": 2, "m5": 5, "m6": 3}
    prefs["p4"] = {"m0": 2, "m2": 3, "m3": 100}
    similarities = calculate_similar_items(prefs)
    print get_recommendations_items(prefs, "p1", similarities)
