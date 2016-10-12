# _*_ coding: UTF-8 _*_
'''
作用：聚类函数
时间：2016-10-12
备注: 第三章
'''

import math

# rownames: 博客的名字
# colnames: 单词
def readfile(filename):
    lines = [line for line in file(filename)]

    # 第一行是标题
    colnames = lines[0].strip().split("\t")[1 : ]
    rownames = []
    data = []
    for line in lines[1 : ]:
        p = line.strip().split("\t")
        # p0是行名
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])

    return rownames, colnames, data

# 这里假设v1和v2有同样数量的分量
def pearson(v1, v2):
    sum1, sum2, sum1_square, sum2_square, psum = 0, 0, 0, 0, 0
    n = len(v1)
    for i in range(n):
        sum1 += v1[i]
        sum2 += v2[i]
        sum1_square += pow(v1[i], 2)
        sum2_square += pow(v2[i], 2)
        psum += v1[i] * v2[i]

    num = psum - sum1 * sum2 / n
    den = math.sqrt((sum1_square - sum1 * sum1 / n) * (sum2_square - sum2 * sum2  / n))
    if den == 0: return 0

    return 1.0 - num / den


# 利用距离计算相似度
# 一次遍历，性能稍微好点
def sim_distance(v1, v2):
    distance = sum(pow(v1[i] - v2[i], 2) for i in range(len(v1)))
    return round(1 - 1 / (1 + math.sqrt(distance)), 2)

# 聚类的类
# left, right指向生成该聚类的两个点, 子聚类
class bicluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

# 分级聚类算法
def hcluster(rows, distance = pearson):
    distances = {}
    cluster_id = -1
    clusters = [bicluster(rows[i], id = i) for i in range(len(rows))]

    while(len(clusters) > 1):
        closest = distance(clusters[0].vec, clusters[1].vec)
        closest_pair = (0, 1)

        # 寻找最小值
        n = len(clusters)
        for i in range(n):
            for j in range(i + 1, n):
                id_i, id_j = clusters[i].id, clusters[j].id
                if (id_i, id_j) not in distances:
                    distances[(id_i, id_j)] = distance(clusters[i].vec, clusters[j].vec)

                if distances[(id_i, id_j)] < closest:
                    closest = distances[(id_i, id_j)]
                    closest_pair = (i, j)

        merge_vec = [(clusters[closest_pair[0]].vec[i] + clusters[closest_pair[1]].vec[i]) / 2.0
        for i in range(len(clusters[i].vec))]

        new_cluster = bicluster(merge_vec, left = clusters[closest_pair[0]],
            right = clusters[closest_pair[1]],
            distance = closest, id = cluster_id)

        cluster_id -= 1
        del clusters[closest_pair[1]]
        del clusters[closest_pair[0]]
        clusters.append(new_cluster)

    print "hcluster finished!"
    return clusters[0]

def test_hcluster():
    rownames, colnames, data = readfile("blogdata.txt")
    print hcluster(data).vec

# 使用-, 空格缩进打印
def print_clusters():
    rownames, colnames, data = readfile("blogdata.txt")

    def print_cluster(clust, n):
        # 以下逗号必须，print加逗号不换行，等到某个print没有逗号时才会换行，或者显式出现"\n"
        # print "test", "test1", "test2" 相当于print "test1", print "test2", print "test3"
        for i in range(n): print " ",
        if clust.id < 0:
            print "-"
        else:
            print rownames[clust.id]

        if clust.left != None: print_cluster(clust.left, n + 1)
        if clust.right != None: print_cluster(clust.right, n + 1)

    print_cluster(hcluster(data), 0)

from PIL import Image, ImageDraw

# 获取高度
def get_height(clust):
    if clust.id >= 0: return 1
    return get_height(clust.left) + get_height(clust.right)

# 计算距离
def get_depth(clust):
    if clust.id >= 0: return 0
    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance

# 画一个节点
def draw_node(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = get_height(clust.left) * 10
        h2 = get_height(clust.right) * 10
        line_width = clust.distance * scaling

        # 垂直线
        draw.line((x, y - h2, x, y + h1), fill = (255, 0, 0))

        # 左边节点
        # 左边节点要用right的height, 可以证明这样画出来的图不会有重叠
        # 如果左右节点减去左边的height，就有可能出现重叠
        draw.line((x, y - h2, x + line_width, y - h2), fill = (255, 0, 0))
        draw_node(draw, clust.left, x + line_width, y - h2, scaling, labels)

        # 右边节点
        draw.line((x, y + h1, x + line_width, y + h1), fill = (255, 0, 0))
        draw_node(draw, clust.right, x + line_width, y + h1, scaling, labels)
    else:
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

# 画树状图
def draw_dendrogram(data, labels):
    clust = hcluster(data)
    h = get_height(clust) * 20
    w = 1200
    depth = get_depth(clust)

    # 因为宽度固定，因此对距离值做调整
    scaling = float(w - 150) / depth

    # 白色背景图片
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.line((0, h / 2, 10, h / 2), fill = (255, 0, 0))
    draw_node(draw, clust, 10, h / 2, scaling, labels)
    img.save("clusters.jpg", "JPEG")

# 根据blog名字聚类
def draw_dendrogram_by_blogs():
    rownames, colnames, data = readfile("blogdata.txt")
    draw_dendrogram(data, rownames)

# 转置矩阵
def rotate_matrix(data):
    new_data = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        new_data.append(newrow)

    return new_data

# 根据单词聚类
def draw_dendrogram_by_words():
    rownames, colnames, data = readfile("blogdata.txt")
    draw_dendrogram(rotate_matrix(data), colnames)

draw_dendrogram_by_words()