def yourgoal(title:str='目标',finish:str='完成！',thegoalprograss:int=114,goal:int=1145,nx:int=0):
    '''
    yourgoal介绍：
    使用百分数去快速显示已完成的目标工作量，同时也可以通过百分数显示剩余的工作量。
    更绝的是，可以使用图形化来表示完成的工作量与未完成的工作量！快速又高效！
    类型可以选择“#”，“$”
    “#”为0（默认值），“$”为1

    *需使用int格式填写
    '''
    import math

    fuhao = ['#','$']
    jc = [0,1]
    if nx not in jc:
        return 'error'
    jgs = thegoalprograss / goal * 100
    jgs = math.ceil(jgs)
    jgstr = str(jgs) + '%'
    jdt1h = {5:title + '|' + fuhao[nx] + fuhao[nx] + '                  '  + jgstr + '                    |' + finish ,10:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '                '  + jgstr + '                    |' + finish ,15:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '              '  + jgstr + '                    |' + finish ,
             20:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '            '  + jgstr + '                    |' + finish ,25:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '          '  + jgstr + '                    |' + finish ,30:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '        '  + jgstr + '                    |' + finish 
             ,35:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '      '  + jgstr + '                    |' + finish ,40:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '    '  + jgstr + '                    |' + finish ,45:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '  '  + jgstr + '                    |' + finish 
             ,50:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + jgstr + '                    |' + finish }
    jdt2h = {55:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + '                  |' + finish ,60:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '                |' + finish ,65:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '              |' + finish ,
             70:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '            |' + finish ,75:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '          |' + finish ,80:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '        |' + finish ,
             85:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '      |' + finish ,90:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '   |' + finish ,95:title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '  |' + finish }
    jg = []
    jg.append(jgstr)
    jg.append(str(100 - jgs) + '%')
    if jgs <= 0 or jgs >= 0 and jgs <= 4:
        jg.append(title + '|                    '  + jgstr + '                    |' + finish )
    for num,prograss in jdt1h.items():
        if jgs >= num and jgs < num + 4:
            jg.append(prograss)
            break
    for num,prograss in jdt2h.items():
        if jgs >= num and jgs < num + 4:
            jg.append(prograss)
            break
    if jgs >= 100:
        jg.append(title + '|' + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx]  + jgstr + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + fuhao[nx] + '|' + finish)
    return jg