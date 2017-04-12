# -*- encoding:utf-8 -*-
import re
import math

NominalResistors = [1.0,1.1,1.2,1.3,1.5,1.6,1.8,2.0,2.2,2.4,2.7,3.0,3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1]
AllNominalResistors = None
AllNominalResistors_1 = None  # 1/AllNominalResistors
ResistorsParalleling = []
ResistorsSeries = []



def ExResistors(r_exp):
    global AllNominalResistors

    AllNominalResistors = [i*r_exp for i in NominalResistors]
    r_exp *= 10
    AllNominalResistors += [i*r_exp for i in NominalResistors]
    r_exp *= 10
    AllNominalResistors += [i*r_exp for i in NominalResistors]

def AddMinToList(tolist,value):
    sortlist = False
    if value[0] == 160:
        pass
    for i in tolist:
        if i[1] == value[0]:
            return
        if i[0] == value[0]:
            if i[2] < value[2]:
                return
            else:
                i[1] = value[1]
                i[2] = value[2]
                sortlist = True

    if sortlist:
        tolist.sort(key=lambda x: x[2])
        return

    if len(tolist) < 10:
        tolist.insert(0,value)
        tolist.sort(key=lambda x: x[2])
    else:
        if value[2] <= tolist[9][2]:
            tolist.insert(0,value)
            tolist.pop()
            tolist.sort(key=lambda x: x[2])
#
def MinNumAndIndexSeries(i1,i2,v):
    v1 = abs(AllNominalResistors[i1] - v)
    v2 = abs(AllNominalResistors[i2] - v)
    min = (i1,v1) if v1 < v2 else (i2,v2)
    return min

def FindNearestValueSeries(t_value):
    global AllNominalResistors
    t = t_value/AllNominalResistors[0]
    index = int(math.log10(t)*24)
    min = MinNumAndIndexSeries(index,index+1,t_value)
    return min


def Series(t_value):
    global ResistorsSeries
    for i in AllNominalResistors:
        if i > t_value:
            break
        t = t_value - i
        if t > AllNominalResistors[0]:
            min = FindNearestValueSeries(t)
            v1 = AllNominalResistors[min[0]]
            AddMinToList(ResistorsSeries,[v1,i,min[1]])
        else:
            min = FindNearestValueSeries(t_value)
            v1 = AllNominalResistors[min[0]]
            AddMinToList(ResistorsSeries,[v1,0,min[1]])


def MinNumAndIndexParalleling(i1,i2,v):
    v1 = abs(AllNominalResistors_1[i1] - v)
    #print("v1={}".format(AllNominalResistors_1[i1] - v))
    v2 = abs(AllNominalResistors_1[i2] - v)
    #print("v2={}".format(AllNominalResistors_1[i2] - v))
    min = (i1,v1) if v1 < v2 else (i2,v2)
    return min

def FindNearestValueParalleling(t_value):
    global AllNominalResistors_1
    t = 1/(t_value*AllNominalResistors[0])
    index = int(len(AllNominalResistors_1)-math.log10(t)*24)
    min = MinNumAndIndexParalleling(index,index-1,t_value)
    return min

def Paralleling(t_value):
    global ResistorsParalleling
    global AllNominalResistors_1
    t_value_1 = 1/t_value
    AllNominalResistors_1 = [1/x for x in AllNominalResistors[::-1]]
    #AllNominalResistors.reverse()
    for i in AllNominalResistors_1:
        if i > t_value_1:
            break
        t = t_value_1 - i

        if t > AllNominalResistors_1[0]:
            min = FindNearestValueParalleling(t)
            v1 = 1/AllNominalResistors_1[min[0]]

            AddMinToList(ResistorsParalleling,[v1,1/i,min[1]])
        else:
            AddMinToList(ResistorsParalleling,[1/i,None,abs(t_value_1 - i)])

    for i in ResistorsParalleling:
        if i[1]:
            i[2] =abs(t_value - i[0]*i[1]/(i[0] + i[1]))
        else:
            i[2] =abs(t_value - i[0])


def ValToString(val):
    if val is None:
        return '   inf'
    if val < 1000:
        return "{: =6.1f}".format(val)
    else:
        return "{: =5.1f}k".format(val/1000)

if __name__ == "__main__":

    while(True):

        str_Value = input("电阻大小：")
        if re.match(r'^[\d\.]+k?$',str_Value):
            r_value_exp = 0
            if 'k' in str_Value:
                r_value_exp = 3
                str_Value = str_Value[:-1]
            R_Value = float(str_Value)
            R_Value *= math.pow(10,r_value_exp)

            r_exp = math.floor(math.log10(R_Value)+0.5) - 2
            r_exp = math.pow(10,r_exp)
            ExResistors(r_exp)
            break
        else:
            print("请输入有效数值")
    Series(R_Value)
    print("串联:")
    for i in ResistorsSeries:
        print("{},{},{}".format(ValToString(i[0]),ValToString(i[1]),ValToString(i[2])))
    Paralleling(R_Value)
    print("并联:")
    for i in ResistorsParalleling:
        print("{},{},{}".format(ValToString(i[0]),ValToString(i[1]),ValToString(i[2])))
