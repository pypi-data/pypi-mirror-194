import playsound
def yourgoal(title:str='目标',finish:str='完成！',thegoalprograss:int=114,goal:int=1145,nx:int=0):
    '''
    yourgoal介绍：
    使用百分数去快速显示已完成的目标工作量，同时也可以通过百分数显示剩余的工作量。
    更绝的是，可以使用图形化来表示完成的工作量与未完成的工作量！快速又高效！
    类型可以选择“#”，“$”
    “#”为0（默认值），“$”为1

    *需使用int格式填写

    功能介绍：
    title：进度条左侧标题
    finish：进度条右侧完成标题
    thegoalprograss：目标已完成量
    goal：订设目标量
    nx：进度条符号格式（目前只有两种）
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
def yourgoalr(title:str='目标',thegoalprograss:int=114,goal:int=1145,nx:int=0,nxs:int=0):
    '''
    
    yourgoalr
    属于yourgoal的改版，功能一样，只不过进度条动了手脚
    效果：
    |$$$$$$$$$$$$$$$$$$$$目标$$$$$$$$$$$$$$$$$$$$|100%/100%
    |$$$$$$$$$$$$$$$$$$$$目标$$$$$$$$$$$$$$$$$$$$|100%/0%
    '''
    #几乎照抄，但格式要大改！
    import math

    fh = ['#','$']
    jc = [0,1]
    jg = []
    if nx not in jc:
        return 'error'
    jgm = thegoalprograss / goal * 100
    jgm = math.ceil(jgm)
    jgstrw = str(jgm) + '%'
    jg.append(jgstrw)
    jgmy = 100 - jgm
    jgmystr = str(jgmy) + '%'
    if nxs == 1:
        jtbs = jgmystr
    else:
        jtbs = '100%'
    jg.append(jtbs)
    jdt1h = {5:'|' + fh[nx] + fh[nx] + '                  ' + title + '                    |' + jgstrw + '/' + jtbs,
               10:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '                ' + title + '                    |' + jgstrw + '/' + jtbs,15:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '              ' + title + '                    |' + jgstrw + '/' + jtbs,
               20:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '            ' + title + '                    |' + jgstrw + '/' + jtbs,25:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '          ' + title + '                    |' + jgstrw + '/' + jtbs,
               30:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '        ' + title + '                    |' + jgstrw + '/' + jtbs,35:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '      ' + title + '                    |' + jgstrw + '/' + jtbs,
               40:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '    ' + title + '                    |' + jgstrw + '/' + jtbs,45:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '  ' + title + '                    |' + jgstrw + '/' + jtbs,
               50:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '' + title + '                    |' + jgstrw + '/' + jtbs}
    jdt2h = {55:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + '                  |' +  jgstrw + '/' +  jtbs ,60:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '                |' +  jgstrw + '/' +  jtbs ,
             65:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '                |' +  jgstrw + '/' +  jtbs ,70:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '              |' +  jgstrw + '/' +  jtbs ,
             75:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '            |' +  jgstrw + '/' +  jtbs ,80:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '          |' +  jgstrw + '/' +  jtbs ,
             85:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '        |' +  jgstrw + '/' +  jtbs ,90:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '    |' +  jgstrw + '/' +  jtbs ,
             95:'|' + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + title + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + fh[nx] + '  |' +  jgstrw + '/' +  jtbs }
    if jgm <= 0 or jgm >= 0 and jgm <= 4:
        jg.append('|                    ' + title + '                    |' + jgstrw + '/' + jtbs)
    for num,jdt in jdt1h.items():
        if jgm >= num and jgm < num + 5:
            jg.append(jdt)
            break
    for num,jdt in jdt2h.items():
        if jgm >= num and jgm < num + 5:
            jg.append(jdt)
            break
    if jgm >= 100:
        jg.append('|' + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx] + title + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx]  + fh[nx] + '|' + jgstrw + '/' + jgmystr)
    return jg
