#-*- coding:utf8 -*-

import jieba

def segment(text):
    seg = []
    stopwordslist = []
    with open("act/data/stopwordslist.txt","r") as f:
        for line in f.readlines():
            stopwordslist.append(line.strip())
    raw_seg = jieba.cut_for_search(text)
    for word in raw_seg:
        if word not in stopwordslist:
            seg.append(word)
    #res = " ".join(seg)
    return seg

