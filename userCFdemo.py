# 将数据集随意分成M份，其中一份作为测试集，另外M-1份作为训练集
# 在训练集上建立用户兴趣模型，并在测试集上对用户行为做出预测，统计出相应的评测指标
import random, math, operator
import pandas as pd
import os

# train的数据结构应该是字典的字典
# 用户1对电影1237打5分对1662打1分，用户2对123打3分
# train = {
#    1：{
#        1237：5，
#        1662：1
#    },
#    2: {
#       123: 3
#    }
# }
#


def main():
    # 导入数据
    ratingDatas = importSmallRatingDatas()
    # 分为训练集和测试集
    train, test = SplitData(ratingDatas, 10, 5, 1)

    print(Recall(train, test, 10))


def importRatingDatas():
    encoding = 'latin1'
    rpath = os.path.abspath('./ml-1m/ratings.dat')
    rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_csv(rpath, sep='::', header=None, names=rnames, encoding=encoding, engine='python',
                          usecols=[0, 1, 2])
    ratingsList = ratings.values.tolist()

    return ratingsList

def importSmallRatingDatas():
    encoding = 'latin1'
    rpath = os.path.abspath('./ml-latest-small/ratings.csv')
    ratings = pd.read_csv(rpath, sep=',', header=0, encoding=encoding, engine='python',
                          usecols=[0, 1, 2])
    ratingsList = ratings.values.tolist()

    return ratingsList


def SplitData(data, M, k, seed):
    test = []
    train = []
    random.seed(seed)
    for user, item, star in data:
        if random.randint(0, M) == k:
            test.append([user, item, star])
        else:
            train.append([user, item, star])

    trainDict = {}
    testDict = {}
    for user, item, star in test:
        if (user in testDict):
            testDict[user][item] = star
        else:
            testDict[user] = {}

    for user, item, star in train:
        if (user in trainDict):
            trainDict[user][item] = star
        else:
            trainDict[user] = {}

    return trainDict, testDict


# 召回率：有多少比例的用户-物品评分记录被包含在了最终的推荐列表

def Recall(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        if user not in test:
            tu = []
        else:
            tu = test[user]
        rank = GetRecommendation(user, train, N)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit / (all * 1.0)


# 准确率：最终推荐列表有多少比例是发生过的用户-物品评分记录

def Precision(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user, train, N)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all += N
    return hit / (all * 1.0)


# 推荐算法的精度：准确率/召回率

# 覆盖率：最终推荐列表中包含多大比例的物品，如果所有物品都被推荐给至少一个用户，那么覆盖率就是100%

def Coverage(train, test, N):
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user].keys():
            all_items.add(item)
        rank = GetRecommendation(user, train, N)
        for item, pui in rank:
            recommend_items.add(item)
    return (len(recommend_items) / len(all_items) * 1.0)


# 新颖度：推荐列表中的物品平均流行度度量推荐结果的新颖度

def Popularity(train, test, N):
    item_popularity = dict()
    for user, items in train.items():
        for item in items.keys():
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1
    ret = 0
    n = 0
    for user in train.keys():
        rank = GetRecommendation(user, train, N)
        for item, pui in rank:
            ret += math.log(1 + item_popularity[item])  # 物品流行度分布满足长尾分布，取对数后流行度平均值更加稳定
            n += 1
    ret /= n * 1.0
    return ret


# 用户相似度（利用余弦相似度计算相似度）

def UserSimilaritySlow(train):
    W = dict()
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue
            W[u][v] = len(train[u] & train[v])  # 二者都评价过的电影数
            W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)  # 除以二者评价过的电影相乘开更号
    return W  # 返回相似度二维矩阵


# 上述算法的耗时将非常恐怖  O(|U|^2)
# 用户相似度算法优化
# 优化思路：
#        依据上述余弦相似度算法中 矩阵中很多值将是0 这一特点
#        我们可以计算出len(train[u] & train[v]) ≠ 0 的用户对(u,v)再对这部分数据进行计算相关度

def UserSimilarity(train):
    # 建立一个物品到用户的倒排表. 对于每一个物品都保存对该物品产生过行为的用户列表（原先是对每一个用户保存该用户产生过行为的物品列表）
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # 计算用户之间共同评分的矩阵
    C = dict()  # 二维 C[u][v] 为u和v这两个用户共同评价过的电影数
    N = dict()  # 单维 N[u] 为u这个用户评价过的电影数
    for i, users in item_users.items():
        for u in users:
            if u not in N:
                N[u] = 0
            else:
                N[u] += 1
            for v in users:
                if u == v:
                    continue
                if u in C:
                    if v in C[u]:
                        C[u][v] += 1
                    else:
                        C[u][v] = 0
                else:
                    C[u] = {}
            # C这个字典存用户U和用户V共同产生行为的物品个数

    W = dict()  # 存用户之间的相似度二维矩阵
    for u, related_user in C.items():
        for v, cuv in related_user.items():
            if u not in W:
                W[u] = {}
            else:
                W[u][v] = cuv / math.sqrt(N[u] * N[v])

    return W


# 如何计算用户u对物品i的感兴趣程度p(u,i)？

# user是用户、train是训练集、W是上面计算出来的用户相似度、K是要选与用户最像的前K个用户来找推荐的电影
def Recommend(user, train, W, K):
    rank = dict()
    interacted_items = train[user]  # 该用户产生过行为的物品集合
    for v, wuv in sorted(W[user].items(), key=operator.itemgetter(1), reverse=True)[
                  0:K]:  # itemgetter(1)表示取位1的值来排，也就是用户相似度来排
        for i, rvi in train[v].items():  # 从与待推荐物品的用户相似度最高的用户算起，找出该用户所有产生过行为的物品
            if i in interacted_items:  # 如果是用户已经产生过行为的物品跳过
                continue
            if i not in rank:
                rank[i] = 0
            else:
                rank[i] += wuv * rvi
    sortedRank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    return sortedRank


def GetRecommendation(user, train, N):
    # 计算用户相似度
    W = UserSimilarity(train)
    recommendMovives = Recommend(user, train, W, 5)[0:N]
    return recommendMovives


# 有些混乱2018/12/27 有点晕 待续


if __name__ == "__main__":
    print('hello')
    main()
    print('bye')
