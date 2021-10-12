import json
import re
import os
import types

global debug
debug = True

listSkill = []
listPotential = []


# 正则匹配关键词模块
def SearchKey(strin, listin):
    keyout = []
    keyoutCN = []
    # 查找标签
    for i in range(len(listin)):
        cz = re.search(listin[i][2], strin)
        if cz:
            keyout.append(listin[i][1])
            keyoutCN.append(listin[i][0])
    if debug is True:
        print('日文标签：', end='')
        print(keyout)
        #print('中文标签：', end='')
        #print(keyoutCN)
    return keyout, keyoutCN


# 卡牌处理
def CardFileSearch(input_file, output_file):
    with open(input_file, 'r+', encoding='UTF-8')as cardfile_input:
        data_list = json.load(cardfile_input)
        cardfile_input.close()

    # 依次对每张卡进行查找关键词
    for i in data_list:
        # 查找日文 关键词
        skill1EffectStr = i.get("Japanese").get("skill1Effect")
        skill2EffectStr = i.get("Japanese").get("skill2Effect")
        nirvanaEffectStr = i.get("Japanese").get("nirvanaEffect")
        potentialAbility1Str = i.get("Japanese").get("potentialAbility1")
        potentialAbility2Str = i.get("Japanese").get("potentialAbility2")
        if debug is True:
            print(skill1EffectStr)
            print(skill2EffectStr)
            print(nirvanaEffectStr)
            print(potentialAbility1Str)
            print(potentialAbility2Str)
        (skill1key, skill1keyCN) = SearchKey(skill1EffectStr, listSkill)
        (skill2key, skill2keyCN) = SearchKey(skill2EffectStr, listSkill)
        (nirvanakey, nirvanaCN) = SearchKey(nirvanaEffectStr, listSkill)
        (potentialAbility1key, potentialAbility1keyCN) = SearchKey(potentialAbility1Str, listPotential)
        (potentialAbility2key, potentialAbility2keyCN) = SearchKey(potentialAbility2Str, listPotential)

        i["Japanese"]["skill1Search"] = skill1key
        i["Chinese"]["skill1Search"] = skill1keyCN

        i["Japanese"]["skill2Search"] = skill2key
        i["Chinese"]["skill2Search"] = skill2keyCN

        i["Japanese"]["nirvanaSearch"] = nirvanakey
        i["Chinese"]["nirvanaSearch"] = nirvanaCN

        i["Japanese"]["potentialSearch1"] = potentialAbility1key
        i["Chinese"]["potentialSearch1"] = potentialAbility1keyCN

        i["Japanese"]["potentialSearch2"] = potentialAbility2key
        i["Chinese"]["potentialSearch2"] = potentialAbility2keyCN

    with open(output_file, 'w', encoding='UTF-8') as cardfile_output:
        cardfile_output.write(json.dumps(data_list, ensure_ascii=False, indent=4))
        cardfile_output.close()
    print("OK")


# 导入关键词
with open('./config/技能&潜能关键词.csv', 'r+', encoding='UTF-8-sig') as keyfile:
    while True:
        lines = keyfile.readline()  # 整行读取数据
        if not lines:
            keyfile.close()
            break
            pass
        strKey = lines.split(',')
        # 导入技能关键词
        if strKey[0] == '[skill]':
            while True:
                lines = keyfile.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                strKey = lines.split(',')
                if (strKey[0] == '\n') or (strKey[0] == ''):
                    break
                    pass
                else:
                    strKey[-1] = strKey[-1].strip()
                    listSkill.append(strKey)
                    pass
        # 导入潜能关键词
        elif strKey[0] == '[potential]':
            while True:
                lines = keyfile.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                strKey = lines.split(',')
                if (strKey[0] == '\n') or (strKey[0] == ''):
                    break
                    pass
                else:
                    strKey[-1] = strKey[-1].strip()
                    listPotential.append(strKey)
if debug is True:
    print("技能关键词：")
    print(listSkill)
    print("潜能关键词：")
    print(listPotential)

# 处理卡牌文件
pathin = './input'  # 文件夹目录
pathout = './output'  # 文件夹目录
files = os.listdir(pathin)  # 得到文件夹下的所有文件名称
for file in files:  # 遍历文件夹
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        print(files)
        CardFileSearch(pathin + '/' + file, pathout + '/' + file)

