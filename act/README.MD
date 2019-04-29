# fasttext简单实践


## 运行环境:

    python3.5

## 依赖工具

* [fastText](https://github.com/facebookresearch/fastText)
* [jieba](https://github.com/fxsjy/jieba)


## 目录结构

```
    project
    │   README.md
    │   cutdata.py #用于把data.txt转换为切割后trained.txt
    │   train.py #模型训练部分
    │   test.py #测试模型
    │
    └───model
    │   │   classify.model #训练出来的模型
    │
    └───data
        │   data.txt #未分词数据
        │   trained.txt #分词后的数据
```