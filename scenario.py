# -*- coding: utf-8 -*-
# @Time    : 2019/04/26
# @Author  : hjt
# @File    : scenario.py
# @Software: PyCharm+python3

from lru import LRU

class Scenario:
    def __init__(self,act,ner,sessionId,lru_dict):
        self.act2slot = {
            'account_transfer':['person','money'],
            'account_detail':['timespan']
        }
        self.act = act
        self.ner = ner
        self.lru_dict = lru_dict
        self.sessionId = sessionId

    def dict_fusion(self,dict1,dict2):
        '''
        eg. old = {'a': 1, 'b': 2}
            new = {'b': 3, 'c': 4}
            dict_fusion(old,new) = {'a': 1, 'b': 3, 'c': 4}
        :param dict1:
        :param dict2:
        :return:dict
        '''
        dict = dict1.copy()
        dict.update(dict2)
        return dict

    def value_completed(self,dict,list):
        '''
        eg. dict = {'person':['小王'],'money':[100.00],'timespan':['2019-04-20 00:00:00','2019-04-21 00:00:00' ]}
            list = ['person','money']
            res = true

            dict = {'person':['小王'],'money':[],'timespan':['2019-04-20 00:00:00','2019-04-21 00:00:00' ]}
            list = ['person','money']
            res = false

        :param dict: 
        :param list: 
        :return: res
        '''
        for item in list:
            if item not in dict.keys():
                return False
            else:
                if len(dict[item]) > 0:
                    pass
                else:
                    return False
        return True

    def chatflow(self):
        #1.意图命中场景
        if self.act in self.act2slot:
            print('1')

        #2.意图没命中场景
        else:
            print('2')
            #2.1 lru有该sessionId对应的cache
            if self.sessionId in self.lru_dict.keys():
                print('2.1')
                act_old = self.lru_dict[self.sessionId]['act']
                slot_old = self.lru_dict[self.sessionId]['slot']
                slot_fusion = self.dict_fusion(slot_old,self.ner)
                #2.1.1 NER能补全cache
                if self.value_completed(slot_fusion,self.act2slot[act_old]):
                    print('2.1.1')
                    del self.lru_dict[self.sessionId]
                    print(act_old,slot_fusion)
                #2.1.2 NER不能补全cache
                else:
                    print('2.1.2')
                    del self.lru_dict[self.sessionId]
                    print('我会查流水和转账，你可以问问我哦！')

            #2.2 lru没有该sessionId对应的cache
            else:
                print('2.2')
                print('我会查流水和转账，你可以问问我哦！')



def main():
    l = LRU(5)
    l['00000000'] = {
        'act':'account_transfer',
        'slot':{
            'person':['小猴'],
            'timespan':[],
            'money':[]
        }
    }
    scenario = Scenario('account_transfer1',{'person':['小王'],'timespan':[],'money':[1.00]},'00000000',l)
    scenario.chatflow()


if __name__ == '__main__':
    main()