# 将数据集随意分成M份，其中一份作为测试集，另外M-1份作为训练集
# 在训练集上建立用户兴趣模型，并在测试集上对用户行为做出预测，统计出相应的评测指标
import random,math

def SplitData(data, M, k, seed):
    test = []
    train = []
    random.seed(seed)
    for user, item in data:
        if random.randint(0, M) == k:
            test.append([user, item])
        else:
            train.append([user, item])
    return train, test


# 召回率：有多少比例的用户-物品评分记录被包含在了最终的推荐列表

def Recall(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user, N)
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
        rank = GetRecommendation(user, N)
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
        rank = GetRecommendation(user, N)
        for item, pui in rank:
            recommend_items.add(item)
    return (len(recommend_items) / len(all_items) *1.0)

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
        rank = GetRecommendation(user, N)
        for item, pui in rank:
            ret += math.log(1 + item_popularity[item]) # 物品流行度分布满足长尾分布，取对数后流行度平均值更加稳定
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
            W[u][v] = len(train[u] & train[v]) # 二者都评价过的电影数
            W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0) # 除以二者评价过的电影相乘开更号
    return W # 返回相似度二维矩阵

# 上述算法的耗时将非常恐怖  O(|U|^2)
# 用户相似度算法优化（依据上述余弦相似度算法中 矩阵中很多值将是0 这一特点）

def UserSimilarity(train):
    # 建立一个物品到用户的倒排表. 对于每一个物品都保存对该物品产生过行为的用户列表
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # 2018-12-17 待续...