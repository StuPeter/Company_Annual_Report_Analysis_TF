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

rule1 = ['环保理念', '环保方针', '环保政策', '环保制度', '环保管理部门',
         '污染控制部门', '环保管理岗位', '环保内控', '环保目标', '环保措施',
         '环境认证', '环境管理体系', '清洁生产', '环保培训', '环保教育',
         '环保教育', '环保培训', '环保专利', '环保课题', '环保自愿协议',
         '环保荣誉称号', '同时设计', '同时施工', '同时投产']
rule2 = ['资源消耗', '资源节约', '节约资源', '万元GDP能耗', ]
rule3 = ['废水排放', '废气排放', '固废处理', '固废处置', '毒性物质排放',
         '噪声排放', '粉尘排放', '废品回收', '废品利用', '废品削减', '废品清理']
rule4 = ['环保研发费', '环保创新费', '节能投入', '环保治理', '环保工程',
         '环保借款', '环保诉讼', '环保罚款', '环保缴费', '环保人工费',
         '环保设备', '环保设施建设与运营费', '环保监测', '排污费', '绿化费',
         '环境保护费']
rule5 = ['环保拨款', '环保补助', '税收减免', '环保补贴', '环保奖励', '环保福利',
         '环保风险', '环保对策', '企业环保要求']
ruleList = [rule1, rule2, rule3, rule4, rule5, ]


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
    print(scoreList)
    print("总分：%d" % (sum(scoreList)))


def eachFile(path):
    """批量读取txt进行赋值"""
    fileNames = os.listdir(path)
    for file in fileNames:
        newDir = path + '/' + file
        if os.path.isfile(newDir):
            print(newDir.split('/')[-1] + '得分情况：')
            scoreRule(newDir)
        else:
            eachFile(newDir)


def main():
    path = r'F:\\Users\\QQT\\Documents\\Python Projects\\Company_Annual_Report_Analysis_TF\\TxT'
    # path = r'E:\QuanQTing Files\Documents\Code\Python Project\Company_Annual_Report_Analysis_TF\TxT'
    # path = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\TxT\社会责任报告\000027深圳能源\000027深圳能源：2014年度社会责任报告.txt'
    # path = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\TxT\年报数据\000027深圳能源\000027深圳能源2014年年度报告-20150327.txt'
    # scoreRule(path)
    eachFile(path)


if __name__ == '__main__':
    main()
