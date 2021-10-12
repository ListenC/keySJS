幻想收束 关键词提取脚本
=============================
* 处理格式：
```json
[
    {
        "Japanese": {
            "skill1": "",
            "skill1Effect": "",
            "skill2": "",
            "skill2Effect": "",
            "nirvana": "",
            "nirvanaEffect": "",
            "potentialAbility1": "",
            "potentialAbility1Effect": "",
            "potentialAbility2": "",
            "potentialAbility2Effect": ""
        },
        "Chinese": {
        }
    }
]
```
* 关键词列表
    > config/技能&潜能关键词.csv

* 方法
    > 需要处理的文件：input/  
  > 处理完成的文件：output/ 

* 备注
> 目前仅匹配技能与潜能的关键词，关键词匹配规则使用正则表达式，直接修改 技能&潜能关键词.csv