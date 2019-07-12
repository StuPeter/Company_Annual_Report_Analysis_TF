#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/7/12
# @Author  : 圈圈烃
# @File    : FileFilter
# @Description:文件筛选
#
#
import xlrd
import os
import re
import shutil


def readXlsx():
    workbook = xlrd.open_workbook('G:\BaiduNetdiskDownload\跑程序所需数据\重污染企业名录720家.xlsx')
    booksheet = workbook.sheet_by_name('重污染行业 分类二（楼主分享版）')
    needList = list()
    for row in range(1, 720):
        needList.append(booksheet.cell(row, 1).value)
    return needList


def eachFile(path, needList):
    """批量读取txt进行赋值"""
    fileNames = os.listdir(path)
    for file in fileNames:
        newDir = path + '/' + file
        if os.path.isfile(newDir):
            # print(newDir)
            try:
                stockCode = re.findall(r'([0|3|6|9][0-9]{5})[-|\u4e00-\u9fa5|A-Za-z|\s]', newDir)[0]
                if stockCode in needList:
                    shutil.copy(newDir, newDir.replace('跑程序所需数据', '筛选'))
                    print(stockCode)
            except Exception as e:
                print("error1:", e)
        else:
            eachFile(newDir, needList)
            try:
                os.mkdir(newDir.replace('跑程序所需数据', '筛选') + '/')
                print(newDir.replace('跑程序所需数据', '筛选') + '/')
            except Exception as e:
                print("error2:", e)


def main():
    path = r'G:\BaiduNetdiskDownload\跑程序所需数据'
    filterPath = r'G:\BaiduNetdiskDownload\筛选'
    needList = readXlsx()
    print(needList)
    eachFile(path, needList)


if __name__ == '__main__':
    main()
