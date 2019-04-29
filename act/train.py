#-*- coding:utf8 -*-

import jieba
import fasttext

class TrainTask(object):
    def __init__(self):
        self.input_file = "act/data/intent_trained.txt"
        self.ouput = "ft_classify.model"
        self.label_prefix = "__label__"
        self.epoch = 20
        self.ws = 2
        self.lr = 0.5
        self.word_ngrams = 1
        self.dim = 100
        self.classifier = None

    def train(self):
        self.classifier = fasttext.supervised(self.input_file,self.ouput,label_prefix=self.label_prefix,epoch=self.epoch,
                                         ws=self.ws,lr=self.lr,word_ngrams=self.word_ngrams,dim=self.dim)


def main():
    train_task = TrainTask()
    train_task.train()
    '''
    input = "请年假你会办理吗"
    text = jieba.cut_for_search(input)
    text = " ".join(text)
    result = train_task.classifier.predict_proba([text], k=2)
    print("预测问题：" + input + "\n")
    print("预测结果：")
    print(result)
    '''

if __name__ == "__main__":
    main()
