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
            #return res
        else:
            tn = TimeNormalizer()
            res = tn.parse(target = text)
            #return res
        self._time = res

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
        #return res
        self._name = res


    def money_extract(self,text):

        res = []
        '''
        segs = pseg.cut(text)
        for word, flag in segs:
            if flag == 'm':
                res.append(word)

        return res
        '''
        res = []
        nm = NumAndMoneyParser(text)
        res = nm.transOnlyMoney()
        #return res
        self._money = res

    def number_extract(self,text):
        res = []
        nm = NumAndMoneyParser(text)
        res = nm.transAllNumber()
        #return res
        self._number = res

    @property
    def time(self):
        return self._time

    @property
    def name(self):
        return self._name

    @property
    def money(self):
        return self._money

    @property
    def number(self):
        return  self._number




def main():
    ex = extractor()
    #time = ex.time_extract("明天上午10点")
    #name = ex.name_extract("给林冠峰转100")
    #money = ex.money_extract("123块")#一二三哈哈哈给小王转二十块
    #number = ex.number_extract("123块")
    ex.time_extract("明天上午10点")
    ex.name_extract("给林冠峰转100")
    ex.money_extract("123块")  # 一二三哈哈哈给小王转二十块
    ex.number_extract("123块")
    print(ex.time)
    print(ex.name)
    print(ex.money)
    print(ex.number)

if __name__ == '__main__':
    main()
