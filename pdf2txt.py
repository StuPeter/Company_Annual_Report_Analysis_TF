#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/7/4
# @Author  : 圈圈烃
# @File    : pdf2txt_2
# @Description:
#
#
# ! python3
# -*- coding: utf-8 -*-

import sys
import importlib
import os

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def parse(readPath, savePath):
    fp = open(readPath, 'rb')  # 以二进制读模式打开
    # fp = urlopen(path)  # 远程文件

    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()

        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():  # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for out in layout:
                if (isinstance(out, LTTextBoxHorizontal)):
                    with open(savePath, 'a+', encoding='utf-8') as f:
                        results = out.get_text()
                        # print(results)
                        f.write(results + '\n')


def eachFile(path):
    """批量转化pdf2txt"""
    fileNames = os.listdir(path)
    for file in fileNames:
        newDir = path + '/' + file
        if os.path.isfile(newDir):
            readPath = newDir
            savePath = readPath.replace('文本数据试图爬虫', 'TxT').replace('pdf', 'txt').replace('PDF', 'txt')
            try:
                parse(readPath, savePath)
                print(savePath.split('/')[-1] + '转化成功...')
            except Exception as e:
                print(readPath + '转化失败！！！')
                print(e)
        else:
            eachFile(newDir)
            try:
                os.mkdir(newDir.replace('文本数据试图爬虫', 'TxT') + '/')
            except Exception as e:
                print(e)


def main():
    path = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\文本数据试图爬虫'
    eachFile(path)


if __name__ == '__main__':
    main()
    # # readPath = r'社会责任报告\000027深圳能源\000027深圳能源：2018年度社会责任报告.PDF'
    # readPath = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\文本数据试图爬虫\年报数据\000027深圳能源\000027深圳能源2018年年度报告-2019.PDF'
    # savePath = readPath.replace('PDF', 'txt').replace('pdf', 'txt')
    # parse(readPath, savePath)
