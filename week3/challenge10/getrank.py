# -*- coding: utf-8 -*-
#! /usr/bin/env python3
import sys
from pymongo import MongoClient
import numpy as np


def get_rank(user_id):
    client = MongoClient('127.0.0.1', 27017)
    db = client.shiyanlou
    contests = db.contests
    uidlist = []
    ranklist = []
    for uid in contests.find():
        uidlist.append(uid['user_id'])
    print('1、先获取所有学员号码： ', uidlist)
    uidlist = list(set(uidlist))
    print('2、然后去掉重复项： ', uidlist)
    print('**此时得到的并非有序列表')
    print('3、用学员号码进行查询，数据库中所有属于这个号码的进行分组')
    for u_id in uidlist:
        userlist = contests.find({'user_id': u_id})
        # print('学员号为：', u_id, '数据为：',)
        # for uu in userlist:
        #     print(uu)
        score = 0
        submit_time = 0
        for x in userlist:
            score += x['score']
            submit_time += x['submit_time']
        ranklist.append([u_id, score, submit_time])
    print('4、再对个学员的数据按照要求进行整合：', ranklist)
    data = np.array(ranklist)
    idex = np.lexsort([data[:, 2], -1 * data[:, 1]])
    sorted_data = data[idex, :]
    print('5、然后用np进行排序')
    print(sorted_data)

    udict = {}
    for index, x in enumerate(sorted_data):
        udict[x[0]] = [index + 1, x[1], x[2]]
    print('6、学员id做key 剩下的数据做value简历字典：')
    print(udict)
    return udict[user_id]

    # 计算用户 user_id 的排名、总分数及花费的总时间

    # 依次返回排名，分数和时间，不能修改顺序
    # return rank, score, submit_time


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Parameter Error')
        exit()
    try:
        user_id = int(sys.argv[1])
    except:
        print('Parameter Error')
        exit()
    # get_rank(user_id)
    userdata = get_rank(user_id)
    print(userdata)
