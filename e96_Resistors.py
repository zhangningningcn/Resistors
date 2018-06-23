# -*- encoding:utf-8 -*-
import math
import re

CharacterExp={"Z":-3,"Y":-2,"X":-1,"A":0,"B":1,"C":2,"D":3,"E":4,"F":5}


def GetInputString():
    code_num = 0
    code_exp = None
    s_type = 0
    while True:
        codestr = input("请输入编码或者电阻值:")
        codestr = codestr.upper()
        if codestr == 'Q':
            return (3,None,None)
        if not re.match(r'^\d\d[A-FX-Z]$',codestr):
            if not re.match(r'^\d+\.?\d*[KM]?$',codestr):
                print("输入代码有误，请重新输入")
                continue
            s_type = 1
        if s_type == 0:
            code_num = int(codestr[:2]) - 1
            if code_num >= 96:
                print("输入代码有误，请重新输入")
                continue
            code_exp = CharacterExp.get(codestr[2],None)
            if code_exp == None:
                print("输入代码有误，请重新输入")
                continue
        else:
            #codestr = codestr.lower()
            if 'K' in codestr:
                code_exp = 3
                codestr = codestr[:-1]
            elif 'M' in codestr:
                code_exp = 6
                codestr = codestr[:-1]
            else:
                code_exp = 0
            code_num = float(codestr)
        break
    return(s_type,code_num,code_exp)
def DecodeResistorE96(code_num,code_exp):

    value = round(math.pow(10,code_num/96),2) * math.pow(10,code_exp+2)
    if value >= 1000000:
        return("{:g}M".format(value/1000000))
    elif value >= 1000:
        return("{:g}k".format(value/1000))
    else:
        return("{:g}".format(value))

def EncodeResistorE96(code_num,code_exp):
    R_Value = code_num * math.pow(10,code_exp)
    log_num = math.log10(R_Value)
    r_exp = math.floor(log_num)
    value = int((log_num - r_exp) * 96 + 0.5)
    value2 = int((log_num - r_exp) * 96)
    if value == value2:
        #d_type = 1
        value2 += 1
    # else:
        # d_type = 2
    if value > 95:
        r_exp1 = int(r_exp) - 1
        value = 0
    else:
        r_exp1 = int(r_exp) - 2
        
    if value2 > 95:
        r_exp2 = int(r_exp) - 1
        value2 = 0
    else:
        r_exp2 = int(r_exp) - 2
    str_exp = None
    for k,v in CharacterExp.items():
        if v == r_exp1:
            str_exp = k
            break
    if str_exp == None:
        return "超范围"
    str_cpde = "{:0=2}{}".format(value+1,str_exp)
    r_str = str_cpde + '(' + DecodeResistorE96(float(value),float(r_exp1)) + ')'
    
    value_x = round(math.pow(10,value/96),2) * math.pow(10,r_exp1+2)
    if abs(R_Value - value_x)/R_Value < 0.005:
        return r_str
        
    str_exp2 = None
    for k,v in CharacterExp.items():
        if v == r_exp2:
            str_exp2 = k
            break
    if str_exp2 != None:
        str_cpde2 = "{:0=2}{}".format(value2+1,str_exp2)
        r_str += '\n' + str_cpde2 + '(' + DecodeResistorE96(float(value2),float(r_exp2)) + ')'
    return r_str



if __name__ == "__main__":
    while True:
        s_type,code_num,code_exp = GetInputString();
        if s_type == 0:
            print(DecodeResistorE96(code_num,code_exp))
        elif s_type == 1:
            print(EncodeResistorE96(code_num,code_exp))
        else:
            break

