# -*- coding: utf-8 -*-
#author : changwei
#date: start from 2019-4-30

import re

class NumAndMoneyParser:
    line = ''
    def __init__(self,line):
        self.line = line
        self.money_str_list = []
        self.trans_only_money_result = []
        self.nums_str_list = []
        self.trans_nums_result = []

    def transOnlyMoney(self):  #one of level one
        self.money_str_list = self.getMoneyStr()
        #print('trans_only_money(): money_str_list',self.money_str_list)
        choose_flag = self.chooseDigitOrCharacter(self.money_str_list)
        #print('choose_digit_or_character():choose_flag',choose_flag)
        result = []   #最终转换后的结果
        if len(self.money_str_list) > 0:
            for idx, item in enumerate(self.money_str_list):
                res = 0.0
                if choose_flag[idx] == 0:
                    res = self.getFromDigitMoney(item)
                elif choose_flag[idx] == 1:
                    res = self.getFromCharMoney(item)
                result.append(res)
        self.trans_only_money_result = result
        return result

    def transAllNumber(self): #one of level one
        self.nums_str_list = self.getNumStr()
        choose_flag = self.chooseDigitOrCharacter(self.nums_str_list)
        #print('choose_digit_or_character():choose_flag', choose_flag)
        result = []  # 最终转换后的结果
        if len(self.nums_str_list) > 0:
            for idx, item in enumerate(self.nums_str_list):
                res = 0.0
                if choose_flag[idx] == 0:
                    res = self.getFromDigitMoney(item)
                elif choose_flag[idx] == 1:
                    res = self.getFromCharMoney(item)
                result.append(res)
        self.trans_nums_result = result
        return result



    def getMoneyStr(self):
        """
        从用户输入中只提取 “转金额”部分
        :return: list of string money
        """
        general_chi_rule_one = r'[转|转账|汇|汇款|打][\.|点|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|0|1|2|3|4|5|6|7|8|9|两|一|二|三|四|五|六|七|八|九|零|十|百|千|万|亿|元|块|毛|角|分]+'
        #general_chi_rule_two = r'[\.|点|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|0|1|2|3|4|5|6|7|8|9|两|一|二|三|四|五|六|七|八|九|零|十|百|千|万|亿|元|块|毛|角|分]+'
        general_chi_pattern_one = re.compile(general_chi_rule_one)
        #general_chi_pattern_two = re.compile(general_chi_rule_two)
        res = re.findall(general_chi_pattern_one, self.line)
        #print('get_money_str(): res:', res)
        if len(res) == 1:
            res = list(res[0])
            for item in res:
                if item in ['转', '账', '汇', '款', '打']:
                    res.remove(item)
            res = ''.join(res)
            return [res]
        else:
            #print("getMoneyStr():我还不太成熟，您的输入可能有误，请规范输入~")
            return []
          #string

    def getNumStr(self):
        """
        从用户输入中提取 所有数字 部分
        :return: list of string money
        """
        rule_year = r'[0|1|2|3|4|5|6|7|8|9|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|两|一|二|三|四|五|六|七|八|九|零|十|百|千|万|亿]+[年]'
        pattern_year = re.compile(rule_year)
        rule_month = r'[0|1|2|3|4|5|6|7|8|9|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|两|一|二|三|四|五|六|七|八|九|零]+[月]'
        pattern_month = re.compile(rule_month)
        rule_day = r'[0|1|2|3|4|5|6|7|8|9|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|两|一|二|三|四|五|六|七|八|九|零]+[日|号]'
        pattern_day = re.compile(rule_day)
        rule_week = r'[礼拜|星期|周][1|2|3|4|5|6|7|壹|贰|叁|肆|伍|陆|柒|日一|二|三|四|五|六|七]'
        pattern_week = re.compile(rule_week)
        rule_money = r'[转|转账|汇|汇款|打]*[\.|点|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|0|1|2|3|4|5|6|7|8|9|两|一|二|三|四|五|六|七|八|九|零|十|百|千|万|亿|元|块|毛|角|分]+'
        pattern_money = re.compile(rule_money)
        #rule_money_two =  r'[\.|点|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|0|1|2|3|4|5|6|7|8|9|两|一|二|三|四|五|六|七|八|九|零|十|百|千|万|亿|元|块|毛|角|分]+'
        #pattern_money_two = re.compile(rule_money_two)

        res_year = re.findall(pattern_year,self.line)
        res_month = re.findall(pattern_month, self.line)
        res_day = re.findall(pattern_day, self.line)
        res_week = re.findall(pattern_week, self.line)
        res_money = re.findall(pattern_money, self.line)
        #res_money_two = re.findall(pattern_money_two, self.line)

        #res_str = res_year + res_month + res_day + res_week + res_money + res_money_two
        res_str = res_year + res_month + res_day + res_week + res_money
        #print('getNumStr(): res_str:',res_str)
        result = []
        for item in res_str:
            tmp = list(item)
            for char in tmp:
                if char in ['年','月','日','号','礼','拜','星','期','周','转','账','汇','款','打']:
                    tmp.remove(char)
            result.append(''.join(tmp))
        #print('getNumStr(): result:', result)
        return result











    def chooseDigitOrCharacter(self, a_list):
        """
        选择汉字解析还是数字解析，对self.money_str_list中的每个 item 进行判断，0：数字处理，1：汉字处理
        :return:
        """
        char_rule = r'[点|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|两|一|二|三|四|五|六|七|八|九|零|十|百|千|万|亿|元|块|毛|角|分]+'
        char_patter = re.compile(char_rule)
        digit_rule = r'[\.|0|1|2|3|4|5|6|7|8|9|0]+[十|百|千|万|亿|元|块|毛|角|分]*'
        digit_patter = re.compile(digit_rule)

        res = []
        if len(a_list) > 0:
            for item in a_list:
                #print('chooseDigitOrCharacter(): item',item)
                #tmp = re.findall(digit_patter, item)
                if len(re.findall(digit_patter, item)) > 0:
                    res.append(0)  #后续做数字处理
                elif len(re.findall(char_patter, item)) > 0:
                    res.append(1)  #后续做汉字处理
                else:
                    pass
                    #print("chooseDigitOrCharacter():我还不太成熟，您的输入可能有误，请规范输入~")
        return res

    def getFromCharMoney(self, line):
        """
        对应原 get_res_money(line)
        :param line: 一个汉字金额串
        :return: 转换后的数字金额 float型
        """
        if len(line) != 0:
            sep = ['块', '元']
            right_money = ''
            left_money = ''
            left_part = 0.0
            right_part = 0.0
            # ori_money = get_general_money(line)
            ori_money = line
            #print('ori_money:', ori_money)
            for item in ori_money:
                if item in sep:
                    idx = line.index(item)
                    left_money = line[0:idx]
                    right_money = line[idx + 1:]
                    break
            if len(left_money) > 0:
                #print('left', left_money)
                left_part = self.getFromCharMoneyLeft(left_money)#getResultForDigit(left_money)
                #print('left_part', left_part)
            if len(right_money) > 0:
                right_part = self.getFromCharMoneyRight(right_money)#get_right_money(right_money)
                # if 只有整数
                # if 只有小数
            # if len(left_money) == 0 and ori_money[-1] not in ['角','毛','分']: #只有整数
            if len(left_money) == 0 and ('角' not in ori_money) and ('毛' not in ori_money) and ('分' not in ori_money):
                left_part = self.getFromCharMoneyLeft(ori_money)
            if len(right_money) == 0 and ('角' in ori_money or '毛' in ori_money or '分' in ori_money):  # 只有小数
                right_part = self.getFromCharMoneyRight(ori_money)
            result = left_part + right_part
        else:
            result = 0.0
        return result

    def getFromCharMoneyLeft(self,a):
        """
        对应 原 getResultForDigit(a)
        :param a: char money 的整数部分
        :return: 整数部分的金额 数字形式 float型
        """
        the_dict = {u'零': 0, u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9, u'十': 10,u'百': 100, u'千': 1000, u'万': 10000,
                    u'０': 0, u'１': 1, u'２': 2, u'３': 3, u'４': 4, u'５': 5, u'６': 6, u'７': 7, u'８': 8, u'９': 9,
                    u'壹': 1, u'贰': 2, u'叁': 3, u'肆': 4, u'伍': 5, u'陆': 6, u'柒': 7, u'捌': 8, u'玖': 9, u'拾': 10,
                    u'佰': 100, u'仟': 1000, u'萬': 10000,u'亿': 100000000, u'两': 2}
        count = 0
        result = 0
        tmp = 0
        Billion = 0
        while count < len(a):
            tmpChr = a[count]  # 从左向右遍历，先读取高位
            # print tmpChr
            tmpNum = the_dict.get(tmpChr, None)
            # 如果等于1亿
            if tmpNum == 100000000:
                result = result + tmp
                result = result * tmpNum
                # 获得亿以上的数量，将其保存在中间变量Billion中并清空result
                Billion = Billion * 100000000 + result
                result = 0
                tmp = 0
            # 如果等于1万
            elif tmpNum == 10000:
                result = result + tmp
                result = result * tmpNum
                tmp = 0
            # 如果等于十或者百，千
            elif tmpNum in [10, 100, 1000]:
                if tmp == 0:
                    tmp = 1
                result = result + tmpNum * tmp
                tmp = 0
            # 如果是个位数
            elif tmpNum is not None:
                if count == 0 and (len(a) - 1) == 0:
                    tmp = tmpNum
                elif count < len(a) - 1 or the_dict.get(a[count - 1], None) == 10:
                    tmp = tmp * 10 + tmpNum
                #elif count == len(a) - 1 and a[count - 1] in ['百', '千', '万', '亿', '佰', '仟', '萬']:
                elif count == len(a) - 1:
                    if a[count - 1] in ['百', '佰']:
                        tmp = tmpNum * 10
                    elif a[count - 1] in ['千', '仟']:
                        tmp = tmpNum * 100
                    elif a[count - 1] in ['万', '萬']:
                        tmp = tmpNum * 1000
                    elif a[count - 1] == '亿':
                        tmp = tmpNum * 10000000
                    else:
                        tmp = tmp * 10 + tmpNum
            count += 1

        result = result + tmp
        result = result + Billion
        return result

    def getFromCharMoneyRight(self, a):
        """
        对应 原 get_right_money(a)
        :param a: char money 的小数部分
        :return: 小数部分的金额 数字形式 float型
        """
        a_dict = {u'零': 0, u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9,
                  u'壹': 1, u'贰': 2, u'叁': 3, u'肆': 4, u'伍': 5, u'陆': 6, u'柒': 7, u'捌': 8, u'玖': 9,
                  u'毛': 0.1, u'分': 0.01, u'角': 0.1, u'点': 0}
        count = 0
        result = 0.0
        tmp = 0.0
        tmpNum = 0.0  # 五毛六分
        while count < len(a):
            tmpNum = a_dict.get(a[count], None)
            if tmpNum == 0.1:
                result = tmp * tmpNum  # 0.5
                tmp = 0.0
            elif tmpNum == 0.01:
                result = result + tmp * tmpNum
                tmp = 0.0
            elif tmpNum is not None:
                if len(a) == 1:
                    result = tmpNum * 0.1
                elif count == len(a) - 1:
                    result = result + tmpNum * 0.01
                else:
                    tmp = tmpNum  # 5
            count += 1
        return result

    def getFromDigitMoney(self,line):
        """
        对应原 get_digit_money(line)
        :param line: 一个数字金额串
        :return: 转换后的数字金额 float型
        """
        dict_one = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                    u'拾': 10, u'佰': 100, u'仟': 1000, u'萬': 10000, u'亿': 100000000,
                    u'十': 10, u'百': 100, u'千': 1000, u'万': 10000, u'.': 0.1, u'点': 0.1, u'毛': 0.1, u'角': 0.1, '分': 0.01}

        if '.' not in line and '点' not in line:
            count = 0  # 字串索引
            result = 0.0
            tmp = 0.0
            Billion = 0.0
            while count < len(line):
                tmpChar = line[count]
                tmpNum = dict_one.get(tmpChar, None)
                if tmpNum == 100000000:
                    result = result + tmp
                    result = result * tmpNum
                    # 获得亿以上的数量，将其保存在中间变量Billion中并清空result
                    Billion = Billion * 100000000 + result
                    result = 0
                    tmp = 0
                elif tmpNum == 10000:
                    result = result + tmp
                    result = result * tmpNum
                    tmp = 0.0
                    # 如果等于十或者百，千
                elif tmpNum in [10, 100, 1000]:
                    if tmp == 0:
                        tmp = 1
                    result = result + tmpNum * tmp
                    tmp = 0
                elif tmpNum is not None:
                    # tmp = tmp*10 + tmpNum
                    if count == 0 and (len(line) - 1) == 0:
                        tmp = tmpNum
                    # elif count < len(line) - 1 or the_dict.get(line[count - 1], None) == 10:
                    # tmp = tmp * 10 + tmpNum
                    elif count == len(line) - 1 and line[count - 1] in ['百', '千', '万', '亿', '佰', '仟', '萬', '块', '元',
                                                                        '分', '角']:
                        if line[count - 1] in ['百', '佰']:
                            tmp = tmpNum * 10
                        if line[count - 1] in ['千', '仟']:
                            tmp = tmpNum * 100
                        if line[count - 1] in ['万', '萬']:
                            tmp = tmpNum * 1000
                        if line[count - 1] == '亿':
                            tmp = tmpNum * 10000000
                        if line[count - 1] in ['块', '元']:
                            tmp = tmpNum * 0.1
                        if line[count - 1] in ['角']:
                            tmp = tmpNum * 0.01
                        if line[count - 1] in ['分']:
                            tmp = tmpNum * 0.01
                    else:
                        tmp = tmp * 10.0 + tmpNum
                count += 1
            result = result + tmp
            result = result + Billion
        else:
            # if '.' in line:
            if '点' in line:
                line = line.replace('点', '.')
            result = 0.0
            rule_one = r'[0|1|2|3|4|5|6|7|8|9|\.]+'
            pattern_one = re.compile(rule_one)
            res = re.findall(pattern_one, line)[0]
            #print('res(.):', res)
            idx = len(res)
            multi = line[idx:]
            #print('multi:', multi)
            # if multiple in ['元','块']:
            #    result = float(res) * 1
            multi_num = 1.0
            for item in multi:
                if item in ['十', '拾']:
                    multi_num *= 10.0
                if item in ['百', '佰']:
                    multi_num *= 100.0
                if item in ['千', '仟']:
                    multi_num *= 1000.0
                if item in ['万', '萬']:
                    multi_num *= 10000.0
                if item in ['亿']:
                    multi_num *= 100000000.0
                if item in ['角', '毛']:
                    multi_num *= 0.1
                if item in ['分']:
                    multi_num *= 0.01
            result = float(res) * multi_num
        return result


if __name__ == "__main__":
    p1 = NumAndMoneyParser("不了，给刘哲转三万八")
    #p1 = NumAndMoneyParser("二零一九")
    #res = p1.transOnlyMoney()  #level one
    #res = p1.getNumStr()
    res = p1.transAllNumber()
    print(res)