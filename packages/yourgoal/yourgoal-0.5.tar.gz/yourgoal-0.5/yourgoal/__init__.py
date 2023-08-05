﻿'''

yourgoal 版本0.5
作者的moneygoal模块废稿改版，重新发送
使用新的方法让其更容易使用
因为此版本是0.5，所以是暂时只有一个函数
待会作者会更新！谢谢使用！
有关帮助链接，请点开这里：https://www.bilibili.com/video/BV1GJ411x7h7/
'''
def yourgoal(thegoalprograss:int=114,goal:int=1145):
    '''
    
    yourgoal介绍：
    使用百分数去快速显示已完成的目标工作量，同时也可以通过百分数显示剩余的工作量。
    更绝的是，可以使用图形化来表示完成的工作量与未完成的工作量！快速又高效！
    *需使用int格式填写
    '''
    import math

    jgs = thegoalprograss / goal * 100
    jgs = math.ceil(jgs)
    jgstr = str(jgs) + '%'
    jdt1h = {5:'赚钱目标|##                  '  + jgstr + '                    |完成！',10:'赚钱目标|####                '  + jgstr + '                    |完成！',15:'赚钱目标|######              '  + jgstr + '                    |完成！',
             20:'赚钱目标|########            '  + jgstr + '                    |完成！',25:'赚钱目标|##########          '  + jgstr + '                    |完成！',30:'赚钱目标|############        '  + jgstr + '                    |完成！'
             ,35:'赚钱目标|##############      '  + jgstr + '                    |完成！',40:'赚钱目标|################    '  + jgstr + '                    |完成！',45:'赚钱目标|##################  '  + jgstr + '                    |完成！'
             ,50:'赚钱目标|####################' + jgstr + '                    |完成！'}
    jdt2h = {55:'赚钱目标|####################'  + jgstr + '##                  |完成！',60:'赚钱目标|####################'  + jgstr + '####                |完成！',65:'赚钱目标|####################'  + jgstr + '######              |完成！',
             70:'赚钱目标|####################'  + jgstr + '########            |完成！',75:'赚钱目标|####################'  + jgstr + '##########          |完成！',80:'赚钱目标|####################'  + jgstr + '############        |完成！',
             85:'赚钱目标|####################'  + jgstr + '##############      |完成！',90:'赚钱目标|####################'  + jgstr + '################   |完成！',95:'赚钱目标|####################'  + jgstr + '##################  |完成！'}
    jg = []
    jg.append(jgstr)
    jg.append(str(100 - jgs) + '%')
    if jgs <= 0 or jgs >= 0 and jgs <= 4:
        jg.append('赚钱目标|                    '  + jgstr + '                    |完成！')
    for num,prograss in jdt1h.items():
        if jgs >= num and jgs < num + 4:
            jg.append(prograss)
            break
    for num,prograss in jdt2h.items():
        if jgs >= num and jgs < num + 4:
            jg.append(prograss)
            break
    if jgs >= 100:
        jg.append('赚钱目标|####################'  + jgstr + '####################|完成！')
    return jg