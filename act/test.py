#-*- coding:utf8 -*-

import jieba
import fasttext
from segment import segment

class InterfaceClassify(object):
    def __init__(self):
        self.model = fasttext.load_model("act/ft_classify.model.bin")
        self.topK = 1
        self.label_prefix = "__label__"
        self.test_file = "act/data/intent_raw_test.txt"

    def classify(self,q):
        #text = jieba.cut_for_search(q)
        text = segment(q)
        text = " ".join(text)
        classifier = self.model
        res = classifier.predict_proba([text],k=self.topK)
        return res

    def get_label_prob(self,li):
        if li[0][0][1] < 0.7:
            label = "other"
        else:
            label = li[0][0][0].replace(self.label_prefix,"")

        prob = li[0][0][1]
        return label, prob

def main():
    interface_classify = InterfaceClassify()

    line_count = 0
    acc_count = 0
    with open(interface_classify.test_file, 'r') as f:
        for line in f.readlines():
            line_count = line_count +1.0
            li = interface_classify.classify(line.split()[0])
            label, prob = interface_classify.get_label_prob(li)
            if (label == line.split()[1].replace(interface_classify.label_prefix,"")):
                acc_count = acc_count +1.0
            else:
                print(line)

        acc = acc_count/line_count

    print("测试集准确率"+str(acc))

    while (1):
        q = input("请输入你的问题：")
        print("问题：" + q)
        li = interface_classify.classify(q)
        label, prob = interface_classify.get_label_prob(li)
        print("类别：" + label + "  概率：" + str(prob))

if __name__ == '__main__':
    main()