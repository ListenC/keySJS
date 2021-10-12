import json
import re
import os
import types

global debug
debug = True


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
def CardFileSearch(input_file, output_file, skillfilter=True, potentialfilter=True, specialfilter=True):
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
        # 进行正则匹配
        if skillfilter is True:
            (skill1key, skill1keyCN) = SearchKey(skill1EffectStr, listSkill)
            (skill2key, skill2keyCN) = SearchKey(skill2EffectStr, listSkill)
            (nirvanakey, nirvanaCN) = SearchKey(nirvanaEffectStr, listSkill)
        if potentialfilter is True:
            (potentialAbility1key, potentialAbility1keyCN) = SearchKey(potentialAbility1Str, listPotential)
            (potentialAbility2key, potentialAbility2keyCN) = SearchKey(potentialAbility2Str, listPotential)
        if specialfilter is True:
            (skill1key_S, skill1keyCN_S) = SearchKey(skill1EffectStr, listSpecial)
            (skill2key_S, skill2keyCN_S) = SearchKey(skill2EffectStr, listSpecial)
            (nirvanakey_S, nirvanaCN_S) = SearchKey(nirvanaEffectStr, listSpecial)

        # 处理json
        if skillfilter is True:
            i["Japanese"]["skill1Search"] = skill1key
            i["Chinese"]["skill1Search"] = skill1keyCN
            i["Japanese"]["skill2Search"] = skill2key
            i["Chinese"]["skill2Search"] = skill2keyCN
            i["Japanese"]["nirvanaSearch"] = nirvanakey
            i["Chinese"]["nirvanaSearch"] = nirvanaCN
        if potentialfilter is True:
            i["Japanese"]["potentialSearch1"] = potentialAbility1key
            i["Chinese"]["potentialSearch1"] = potentialAbility1keyCN
            i["Japanese"]["potentialSearch2"] = potentialAbility2key
            i["Chinese"]["potentialSearch2"] = potentialAbility2keyCN
        if specialfilter is True:
            i["Japanese"]["skill1SearchS"] = skill1key_S
            i["Chinese"]["skill1SearchS"] = skill1keyCN_S
            i["Japanese"]["skill2SearchS"] = skill2key_S
            i["Chinese"]["skill2SearchS"] = skill2keyCN_S
            i["Japanese"]["nirvanaSearchS"] = nirvanakey_S
            i["Chinese"]["nirvanaSearchS"] = nirvanaCN_S

    with open(output_file, 'w', encoding='UTF-8') as cardfile_output:
        cardfile_output.write(json.dumps(data_list, ensure_ascii=False, indent=4))
        cardfile_output.close()
    print("OK")


# 导入关键词
def InputSkill(input_file, input_name, input_list):
    strKey = ''
    with open('./config/' + input_file, 'r+', encoding='UTF-8-sig') as keyfile:
        while True:
            lines = keyfile.readline()  # 整行读取数据
            if not lines:
                keyfile.close()
                break
                pass
            strKey = lines.split(',')
            # 导入关键词
            if strKey[0] == input_name:
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
                        input_list.append(strKey)

    if debug is True:
        print("关键词" + input_name + "列表：")
        print(input_list)


# 处理卡牌文件
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    listSkill = []
    listPotential = []
    listSpecial = []

    InputSkill('技能&潜能关键词.csv', '[skill]', listSkill)                    # 导入技能关键词
    InputSkill('技能&潜能关键词.csv', '[potential]', listPotential)            # 导入潜能关键词
    InputSkill('作用范围&发生条件&威力与特攻关键词.csv', '[发生条件]', listSpecial)       # 导入发生条件关键词
    InputSkill('作用范围&发生条件&威力与特攻关键词.csv', '[敌作用范围]', listSpecial)      # 导入敌作用范围关键词
    InputSkill('作用范围&发生条件&威力与特攻关键词.csv', '[我方作用范围]', listSpecial)     # 导入我方作用范围关键词
    InputSkill('作用范围&发生条件&威力与特攻关键词.csv', '[威力和特攻]', listSpecial)      # 导入威力和特攻关键词
    pathin = './input'  # 文件夹目录
    pathout = './output'  # 文件夹目录
    files = os.listdir(pathin)  # 得到文件夹下的所有文件名称
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            print(files)
            CardFileSearch(pathin + '/' + file, pathout + '/' + file)

