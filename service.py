# -*- coding: utf-8 -*-
# @Time    : 2019/04/29
# @Author  : hjt
# @File    : service.py
# @Software: PyCharm+python3

from act.test import *
from ner.ner_extractor import *
from scenario import *
import json
from lru import LRU
from threading import Thread

class Service():
    def __init__(self):
        self.label2act = {
            'liushui':'account_detail',
            'zhuanzhang':'account_transfer',
            'nianjia':'year_holiday',
            'other':'other'
        }

    def act_recg(self,text):
        act_classifier = InterfaceClassify()
        li = act_classifier.classify(text)
        label,prob = act_classifier.get_label_prob(li)
        return self.label2act[label]

    def ner_extract(self,text):
        ner_ex = extractor()

        t1 = Thread(target=ner_ex.time_extract,args=(text,))
        t1.start()
        t2 = Thread(target=ner_ex.name_extract,args=(text,))
        t2.start()
        t3 = Thread(target=ner_ex.money_extract,args=(text,))
        t3.start()
        t4 = Thread(target=ner_ex.number_extract, args=(text,))
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        #time = ner_ex.time_extract(text)
        #name = ner_ex.name_extract(text)
        #money = ner_ex.money_extract(text)
        res = {
            #'time':time,
            #'name':name,
            #'money':money
            'time': ner_ex.time,
            'name':ner_ex.name,
            'money':ner_ex.money,
            'number':ner_ex.number
        }
        return res

def main():
    l = LRU(5)
    service = Service()
    while (1):
        query = input('> 请输入问题：')
        act = service.act_recg(query)
        ner = service.ner_extract(query)
        #print (act,ner)
        timespan = json.loads(ner['time'])['timespan']
        person = ner['name']
        money = ner['money']
        number = ner['number']
        slot = {
            'timespan':timespan,
            'person':person,
            'money':money,
            'number':number
        }

        scenario = Scenario(act,slot,'00000000',l)
        res = scenario.chatflow()
        print (res)
        #print(l)



if __name__ == '__main__':
    main()