#-*- coding:utf8 -*-

import jieba
from segment import segment


def main():
    '''
    input:
        inFile eg.: "今年三月份流水信息	__label__liushui"
    output:
        outFile eg.: "今年 三月 月份 三月份 流水 信息 __label__liushui"
    '''
    inFile = 'data/intent_raw_train.txt'
    outFile = 'data/intent_trained.txt'


    for i in range(len(inFile)):
        f = open(inFile,'r')
        writer = open(outFile,'w')
        for line in f.readlines():
            splitor = line.split()
            #text = jieba.cut_for_search(splitor[0])
            text = segment(splitor[0])
            text = " ".join(text) + " " + splitor[1] + '\n'
            writer.writelines(text)
        f.close()
        writer.close()

if __name__ == '__main__':
    main()