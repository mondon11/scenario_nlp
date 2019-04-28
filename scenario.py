# -*- coding: utf-8 -*-
# @Time    : 2019/04/26
# @Author  : hjt
# @File    : scenario.py
# @Software: PyCharm+python3

from lru import LRU
import json

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

        #去除dict里value的len是0的项
        dict1_cp = dict1.copy()
        dict2_cp = dict2.copy()
        for item in dict1_cp.keys():
            if len(dict1[item]) == 0:
                dict1.pop(item)
        for item in dict2_cp.keys():
            if len(dict2[item]) == 0:
                dict2.pop(item)

        dict = dict1.copy()
        dict.update(dict2)
        return dict

    def value_completed(self,dict,list):
        '''
        eg. dict = {'person':['小王'],'money':[100.00],'timespan':['2019-04-20 00:00:00','2019-04-21 00:00:00' ]}
            list = ['person','money']
            res = true,[]

            dict = {'person':['小王'],'money':[],'timespan':['2019-04-20 00:00:00','2019-04-21 00:00:00' ]}
            list = ['person','money']
            res = false,['money']

        :param dict: 
        :param list: 
        :return:
        '''
        res = []
        flag = True
        for item in list:
            if item not in dict.keys():
                res.append(item)
                flag=False
            else:
                if len(dict[item]) > 0:
                    pass
                else:
                    res.append(item)
                    flag = False
        return flag,res

    def chatflow(self):
        #1.意图命中场景
        if self.act in self.act2slot:
            print('1')
            #1.1 lru有该sessionId对应的cache
            if self.sessionId in self.lru_dict.keys():
                print('1.1')
                #1.1.1 新老act一致
                if self.act == self.lru_dict[self.sessionId]['act']:
                    print('1.1.1')
                    slot_fusion = self.dict_fusion(self.lru_dict[self.sessionId]['slot'],self.ner)
                    completed,missed = self.value_completed(slot_fusion,self.act2slot[self.act])
                    #1.1.1.1 新老NER融合后必填slot可补全
                    if completed:
                        print('1.1.1.1')
                        print(self.act,slot_fusion)
                        del self.lru_dict[self.sessionId]
                    #1.1.1.2 新老NER融合后必填slot不能补全
                    else:
                        print('1.1.1.2')
                        del self.lru_dict[self.sessionId]
                        self.lru_dict[self.sessionId] = {
                            'act':self.act,
                            'slot':slot_fusion
                        }
                        print('请补全如下信息：' + str(missed))
                #1.1.2 新老act不一致
                else:
                    print('1.1.2')
                    completed,missed = self.value_completed(self.ner,self.act2slot[self.act])
                    #1.1.2.1 新NER能补全必填slot
                    if completed:
                        print('1.1.2.1')
                        print(self.act,self.ner)
                        del self.lru_dict[self.sessionId]
                    #1.1.2.2 新NER不能补全必填slot
                    else:
                        print('1.1.2.2')
                        del self.lru_dict[self.sessionId]
                        self.lru_dict[self.sessionId] = {
                            'act':self.act,
                            'slot':self.ner
                        }
                        print(self.lru_dict)
                        print('请补全如下信息：' + str(missed))
            #1.2 lru没有该sessionId对应的cache
            else:
                print('1.2')
                completed,missed = self.value_completed(self.ner,self.act2slot[self.act])
                #1.2.1 NER能补全必填slot
                if completed:
                    print('1.2.1')
                    print(self.act,self.ner)
                #1.2.2 NER不能补全必填slot
                else:
                    print('1.2.2')
                    self.lru_dict[self.sessionId] = {
                        'act':self.act,
                        'slot':self.ner
                    }
                    print('请补全如下信息：'+str(missed))


        #2.意图没命中场景
        else:
            print('2')
            #2.1 lru有该sessionId对应的cache
            if self.sessionId in self.lru_dict.keys():
                print('2.1')
                act_old = self.lru_dict[self.sessionId]['act']
                slot_old = self.lru_dict[self.sessionId]['slot']
                slot_fusion = self.dict_fusion(slot_old,self.ner)
                completed,missed = self.value_completed(slot_fusion,self.act2slot[act_old])
                #2.1.1 NER能补全cache
                if completed:
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
    '''
    l['00000000'] = {
        'act':'account_transfer',
        'slot':{
            'person':['小猴'],
            'timespan':[],
            'money':[]
        }
    }
    '''
    # eg. input: ["account_detail",{"person":["ss"],"timespan":[],"money":[]},"00000000"]
    while(1):
        query = input('请输入问题：')
        ls = json.loads(query)
        scenario = Scenario(ls[0],ls[1],ls[2],l)
        #scenario = Scenario('account_detail',{'person':['ss'],'timespan':[],'money':[]},'00000000',l)
        scenario.chatflow()
        print(l)

if __name__ == '__main__':
    main()