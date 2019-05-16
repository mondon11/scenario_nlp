# -*- coding: utf-8 -*-
# @Time    : 2019/04/29
# @Author  : hjt
# @File    : ner.py
# @Software: PyCharm+python3

from ner.time.TimeNormalizer import *
import jieba.posseg as pseg

class extractor():
    def __init__(self):
        pass

    def time_extract(self,text):
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
        segs = pseg.cut(text)
        for word,flag in segs:
            if flag == 'nr':
                res.append(word)
        #return res
        self._name = res

    def money_extract(self,text):
        res = []
        segs = pseg.cut(text)
        for word, flag in segs:
            if flag == 'm':
                res.append(word)
        #return res
        self._money = res

    @property
    def time(self):
        return self._time

    @property
    def name(self):
        return self._name

    @property
    def money(self):
        return self._money


def main():
    ex = extractor()
    time = ex.time_extract("明天上午10点")
    name = ex.name_extract("给林冠峰转100")
    print(time)
    print(name)

if __name__ == '__main__':
    main()
