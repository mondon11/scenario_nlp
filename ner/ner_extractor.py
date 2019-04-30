# -*- coding: utf-8 -*-
# @Time    : 2019/04/29
# @Author  : hjt
# @File    : ner.py
# @Software: PyCharm+python3

from ner.time.TimeNormalizer import *
import jieba.posseg as pseg
from pyhanlp import *
from num_money_parser import *

class extractor():
    def __init__(self):
        pass

    def time_extract(self,text):
        res = {}
        if text == '':
            res = {"error": "text is null", "timestamp": "", "timespan": [], "timedelta": ""}
            return res
        else:
            tn = TimeNormalizer()
            res = tn.parse(target = text)
            return res

    def name_extract(self,text):
        res = []
        '''
        segs = pseg.cut(text)  
        for word,flag in segs:
            if flag == 'nr':
                res.append(word)
        return res
        '''

        for item in HanLP.segment(text):
            if str(item.nature) == 'nr':
                res.append(str(item.word))
        return res


    def money_extract(self,text):
        '''
        res = []
        segs = pseg.cut(text)
        for word, flag in segs:
            if flag == 'm':
                res.append(word)
        return res
        '''
        res = []
        nm = NumAndMoneyParser(text)
        res = nm.transOnlyMoney()
        return res


    def number_extract(self,text):
        res = []
        nm = NumAndMoneyParser(text)
        res = nm.transAllNumber()
        return res


def main():
    ex = extractor()
    time = ex.time_extract("明天上午10点")
    name = ex.name_extract("给林冠峰转100")
    money = ex.money_extract("123块")#一二三哈哈哈给小王转二十块
    number = ex.number_extract("123块")
    print(time)
    print(name)
    print(money)
    print(number)

if __name__ == '__main__':
    main()
