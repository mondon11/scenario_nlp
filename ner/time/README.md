## 简介
Time-NLP的python3版本   
python 版本https://github.com/sunfiyes/Time-NLPY  
Java 版本https://github.com/shinyke/Time-NLP
## 功能说明
用于句子中时间词的抽取和转换  
详情请见test.py

    res = tn.parse(target=u'过十分钟') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'2013年二月二十八日下午四点三十分二十九秒', timeBase='2013-02-28 16:30:29') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'我需要大概33天2分钟四秒', timeBase='2013-02-28 16:30:29') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'今年儿童节晚上九点一刻') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'2个小时以前') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
    res = tn.parse(target=u'晚上8点到上午10点之间') # target为待分析语句，timeBase为基准时间默认是当前时间
    print(res)
返回结果：

    {"timedelta": "0 days, 0:10:00", "type": "timedelta"}
    {"timestamp": "2013-02-28 16:30:29", "type": "timestamp"}
    {"type": "timedelta", "timedelta": {"year": 0, "month": 1, "day": 3, "hour": 0, "minute": 2, "second": 4}}
    {"timestamp": "2018-06-01 21:15:00", "type": "timestamp"}
    {"error": "no time pattern could be extracted."}
    {"type": "timespan", "timespan": ["2018-03-16 20:00:00", "2018-03-16 10:00:00"]}
    
## 使用方式 
demo：python3 Test.py

优化说明
    
| 问题          | 以前版本                                     | 现在版本                    |
| ----------- | ---------------------------------------- | ---------------------- |
| 无法解析下下周末     | "timestamp": "2018-04-01 00:00:00"                                    | "timestamp": "2018-04-08 00:00:00"                 |
| 无法解析 3月4         | "2018-03-01"                                   | "2018-03-04"               |
| 无法解析 初一 初二      | cannot parse                                    | "2018-02-16"              |
| 晚上8点到上午10点之间  无法解析上午      | ["2018-03-16 20:00:00", "2018-03-16 22:00:00"] |  ["2018-03-16 20:00:00", "2018-03-16 10:00:00"]|
| 3月21号  错误解析成2019年      | "2019-03-21" | "2018-03-21" |

感谢@[tianyuningmou](https://github.com/tianyuningmou) 目前增加了对24节气的支持


    temp = ['今年春分']
    "timestamp" : "2020-03-20 00:00:00"

## TODO

| 问题          | 现在版本                                     | 正确
| ----------- | ---------------------------------------- | ---------------------- |
| 晚上8点到上午10点之间     |  ["2018-03-16 20:00:00", "2018-03-16 22:00:00"] |  ["2018-03-16 20:00:00", "2018-03-17 10:00:00"]"                                    | "timestamp": "2018-04-08 00:00:00"                 |

## 金融场景改造
如查流水记录场景，需要给出timespan而非timestamp。如“我要查上个月的流水记录”，结果应该为{"timespan": ["2019-03-01 00:00:00", "2019-04-01 00:00:00"]}。因此需要做改造。  
0.源程序的默认timebase是当前时间，导致时间向后查询。如今天是2019-04-28 10：00：00,“1号”解析为2019-05-01,“3月”解析为2020-03-01。与“查历史流水”场景不匹配，需要进行改造。  
	-->只需在TimeNormalizer类初始化时将isPreferFuture置为False
1.以“日”为单位的，timespan应截至到下一天0点。如“3日”、“3号”、“4月3”等，结果应该为{"timespan": ["2019-04-03 00:00:00", "2019-04-04 00:00:00"]}。  
2.以“月”为单位的，timespan应截至到下一月一号0点。如“3月”、“2019.3”等，结果应该为{"timespan": ["2019-03-01 00:00:00", "2019-04-01 00:00:00"]}。  
3.以“年”为单位的，timespan应截止到下一年1月1号0电。如“去年”、“2018年”等，结果应该为{"timespan": ["2018-01-01 00:00:00", "2019-01-01 00:00:00"]}。  
	-->1.2.3在parse()方法进行了改造





