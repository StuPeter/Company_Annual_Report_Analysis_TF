#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/7/11
# @Author  : 圈圈烃
# @File    : KeywordTrain
# @Description:
#
#
from gensim.models import word2vec
import gensim
import logging
import jieba
import os


def cut_txt(filePath):
    """文本语料预处理"""
    newFilePath = filePath.replace('.txt', '_cut.txt')
    with open(filePath, 'r', encoding='utf-8') as fr:
        content = fr.read()
    content = jieba.cut(content, cut_all=False)  # 精确模式
    str_out = ' '.join(content).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
        .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
        .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
        .replace('’', '')  # 去掉标点符号
    with open(newFilePath, 'w', encoding='utf-8') as fw:
        fw.write(str_out)
    return newFilePath


def train_model(filePath, modelSavePath):
    """训练模型"""
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(filePath)  # 加载语料
    model = gensim.models.Word2Vec(sentences, sg=1, size=200, window=5)
    model.save(modelSavePath)
    model.wv.save_word2vec_format(modelSavePath + '.bin', binary=True)  # 以二进制类型保存模型以便重用


def main():
    filePaht = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\yitiantulongji_jinyong.txt'
    newFilePath = cut_txt(filePaht)
    modelSavePath = filePaht.replace('.txt', '.model')
    if not os.path.exists(modelSavePath):
        train_model(newFilePath, modelSavePath)
        print("模型训练完毕...")
    else:
        print("模型已经存在...")

    # 加载模型
    model = word2vec.Word2Vec.load(modelSavePath)
    y = model.most_similar("张三丰", topn=10)
    for item in y:
        print(item[0], item[1])


if __name__ == '__main__':
    main()
