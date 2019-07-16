#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/7/10
# @Author  : 圈圈烃
# @File    : ReportAnalysis
# @Description:
#
#
import os
import jieba
import jieba.analyse
import csv
import re
import operator
import shutil

rule1 = ['环保理念', '环保方针', '环保政策', '环保制度', ]
rule2 = ['环保管理部门', '污染控制部门', '环保管理岗位', '环保内控', ]
rule3 = ['环保目标', '环保措施', ]
rule4 = ['环境认证', '环境管理体系', ]
rule5 = ['清洁生产', ]
rule6 = ['培训', '教育', '环保教育', '环保培训', ]
rule7 = ['环境专利', '环保专利', '环保课题', ]
rule8 = ['自愿协议', ]
rule9 = ['荣誉称号', ]
rule10 = ['同时设计', '同时施工', '同时投产']
# "================================================"
rule11 = ['资源消耗', '资源节约', '节约资源', '节约', '消耗', '资源', ]
rule12 = ['GDP能耗', ]
# "================================================"
rule13 = ['废水', '污水', ]
rule14 = ['废气', ]
rule15 = ['毒性', ]
rule16 = ['噪声', '粉尘', ]
rule17 = ['固废', '处理', '处置', ]
rule18 = ['回收', '废品', '利用', '削减', '清理']
# "================================================"
rule19 = ['环保研发费', '环保创新费', '节能投入', '环境研发', '创新', '节能']
rule20 = ['环保治理', '环保工程', '环保借款', '环境工程', '环境治理']
rule21 = ['环保诉讼', '环保罚款', '环保缴费', '环保人工费', '环境缴费', '环境费用', '环境罚款']
rule22 = ['环保设备', '环保设施建设与运营费', '环保监测', ]
rule23 = ['排污费', '绿化费', '保护费']
rule24 = ['环保拨款', '环保补助', '税收减免', '环保补贴', ]
rule25 = ['环保奖励', ]
rule26 = ['环境福利', ]
rule27 = ['环境风险', '对策', '环保要求']
# "================================================"
ruleList = [rule1, rule2, rule3, rule4, rule5,
            rule6, rule7, rule8, rule9, rule10,
            rule11, rule12, rule13, rule14, rule15,
            rule16, rule17, rule18, rule19, rule20,
            rule21, rule22, rule23, rule24, rule25,
            rule26, rule27, ]


def combineFile(path):
    '''合并文件'''
    sameList = list()
    stockCodeList = list()
    stockPathList = list()
    fileNames = os.listdir(path)
    # 获取同名同年的报告路径
    for file in fileNames:
        newDir = path + '/' + file
        if os.path.isfile(newDir):
            stockCode = re.findall(r'([0|3|6|9][0-9]{5})[-|\u4e00-\u9fa5|A-Za-z|\s]', newDir)[0]
            stockYear = re.findall(r'20[0-1][0-9]', newDir)[0]
            stockCodeList.append([stockCode, stockYear])
            # stockYearList.append(stockYear)
            stockPathList.append(newDir)
        else:
            eachFile(newDir)
    for idx, code1 in enumerate(stockCodeList):
        same = [idx]
        for jdx, code2 in enumerate(stockCodeList):
            if operator.eq(code1, code2):
                # print(idx, jdx)
                same.append(jdx)
        same = list(set(same))
        # print(same)
        sameList.append(same)
    sameList = list(set([tuple(t) for t in sameList]))
    sameList = [list(v) for v in sameList]
    print(sameList)
    # sameList = [[4975]]
    # 合并txt
    for path in sameList:
        if len(path) == 1:
            shutil.copy(stockPathList[path[0]], stockPathList[path[0]].replace("公司合并", "合并后"))
            print(stockPathList[path[0]] + "复制成功...")
        else:
            content = ""
            for index in path:
                filePath = stockPathList[index]
                with open(filePath, 'r', encoding='utf-8') as fr:
                    content += fr.read()
            with open(filePath.replace("公司合并", "合并后"), 'w', encoding='utf-8') as fw:
                fw.write(content)
                print(filePath + "合并成功...")


    # print(stockPathList[3660], stockPathList[3668])
    # print(stockPathList[3569], stockPathList[3570])
    # # print(stockPathList[591], stockPathList[595], stockPathList[596], stockPathList[597], stockPathList[605],
    # #       stockPathList[606], stockPathList[607])


def scoreRuleJieba(path):
    with open(path, 'r', encoding='utf-8') as fr:
        content = fr.read().replace('\n', '').replace(' ', '')
    print(content)
    keywords = jieba.analyse.textrank(content, topK=20, withWeight=True)
    for item in keywords:
        print(item[0], item[1])


def scoreRule(path):
    scoreList = list()
    with open(path, 'r', encoding='utf-8') as fr:
        content = fr.read().replace('\n', '').replace(' ', '')
    for rule in ruleList:
        score = 0
        for keword in rule:
            if keword in content:
                score += 1
        scoreList.append(score)
    # print(scoreList)
    # print("总分：%d" % (sum(scoreList)))
    return sum(scoreList)


def eachFile(path):
    """批量读取txt进行赋值"""
    data = list([['999999', '2012', '2013', '2014', '2015', '2016', '2017', '2018']])
    fileNames = os.listdir(path)
    for file in fileNames:
        newDir = path + '/' + file
        if os.path.isfile(newDir):
            print(newDir.split('/')[-1] + '得分情况：')
            score = scoreRule(newDir)  # 打分函数
            data = write_csv(data, newDir, score)
        else:
            eachFile(newDir)
    with open("整合后_score.csv", "a", newline="", encoding='utf_8_sig') as fw:
        f_csv = csv.writer(fw)
        for row in data:
            f_csv.writerow(row)
        print("csv写入成功...")


def write_csv(data, filePath, score):
    #  ['000000', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    yearList = ['999999', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    rows = ['000000', '', '', '', '', '', '', '']
    stockCode = re.findall(r'([0|3|6|9][0-9]{5})[-|\u4e00-\u9fa5|A-Za-z|\s]', filePath)[0]
    stockIndex = 0
    for j in range(len(data)):
        if stockCode in data[j][0]:
            stockIndex = j
            data[j][0] = str(stockCode) + '\r'
            break
    if stockIndex == 0:
        rows[0] = str(stockCode) + '\r'
        for i in range(8):
            if yearList[i] in filePath:
                rows[i] = str(score)
                break
        data.append(rows)
    else:
        for i in range(8):
            if yearList[i] in filePath:
                data[stockIndex][i] = str(score)
                break
    # print(data)
    return data


def main():
    path = r'G:\BaiduNetdiskDownload\TXT\合并后'
    eachFile(path)
    # combineFile(path)


if __name__ == '__main__':
    main()
