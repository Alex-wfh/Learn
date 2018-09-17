#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
题目1：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？
"""
def exercise1_1() :
    intList = [1, 2, 3, 4]
    totalCnt = 0
    for i in intList :
        for j in intList :
            for k in intList :
                if i != j != k != i :
                #if i != j and i != k and j != k:
                    print ( i*100+j*10+k )
                    totalCnt += 1
    print ( "TotalCnt is : %s" %totalCnt )

def exercise1_2() :
    intList = [1, 2, 3, 4]
    totalCnt = 0
    for i in intList :
        jList = intList.copy()
        jList.remove(i)
        for j in jList :
            kList = jList.copy()
            kList.remove(j)
            for k in kList :
                print ( i*100+j*10+k )
                totalCnt += 1
    print ( "TotalCnt is : %s" %totalCnt )

def exercise1_3():
    from itertools import permutations
    intList = [1, 2, 3, 4]
    totalCnt = 0
    for i in permutations(intList, 3):
        totalCnt += 1
        print(i)
    print( "TotalCnt is : %s" %totalCnt )

"""
题目2：企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；60万到100万之间时，高于60万元的部分，可提成1.5%，高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？
"""
def exercise2_1() :
    def getBonus(performance):
        bonus = 0
        if performance > 100000 :
            bonus += 100000 * 0.1
            if performance > 200000 :
                bonus += (200000 - 100000) * 0.075
                if performance > 400000 :
                    bonus += (400000 - 200000) * 0.05
                    if performance > 600000 :
                        bonus += (600000 - 400000) * 0.03
                        if performance > 1000000 :
                            bonus += (1000000 - 600000) * 0.015
                            bonus += (performance - 1000000) * 0.01
                        else :
                            bonus += (performance - 600000) * 0.015
                    else :
                        bonus += (performance - 400000) * 0.03
                else :
                    bonus += (performance - 200000) * 0.05
            else :
                bonus += (performance - 100000) * 0.075
        else :
            bonus += performance * 0.1
        return bonus

    performance = 120000
    bonus = getBonus( performance )
    print ( "%s 利润，奖金为：%s" %( performance, bonus ) )
    

def exercise2_2() :
    def getBonus( performance ) :
        bonus = 0
        arr = [1000000, 600000, 400000, 200000, 100000, 0]
        rat = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
        for idx, val in enumerate(arr) :
            if performance > val :
                bonus += ( performance - val ) * rat[idx]
                performance = val
        return bonus

    performance = 120000
    bonus = getBonus( performance )
    print ( "%s 利润，奖金为：%s" %( performance, bonus ) )


"""
题目3：一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？
"""
def exercise3() :
    import math
    """
        设整数位x,第一个完全平方数是n^2,第二个完全平方数是m^2
        (x+100)=n^2
        (x+268)=m^2
        m^2-n^2=168
        (m+n)(m-n)=168
        m+n;m-n同为偶数，且m+n>m-n
    """
    for i in range( int( math.sqrt(168) ) )[2::2]:
        if 168 % i == 0 and ( 168 / i ) % 2 == 0 :
            m = ( 168 / i + i ) / 2
            x = m ** 2 - 268
            print ( int(x) )

"""
题目4：输入某年某月某日，判断这一天是这一年的第几天？
"""
def exercise4() :
    year = int(input('year:\n'))
    month = int(input('month:\n'))
    day = int(input('day:\n'))
    baseDayCnt = [ 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30 ]
    # 判断闰年
    def getLeapYearDayCnt( year ) :
        if year % 100 == 0 :
            if year % 400 == 0 : 
                baseDayCnt[1] = 29
        else :
            if year % 4 == 0 :
                baseDayCnt[1] = 29
    print ( "it is the %d th day." % ( sum( baseDayCnt[:month] ) + day ) )
        
"""
题目5：输入三个整数x,y,z，请把这三个数由小到大输出。
"""
def exercise5() :
    x = int( input("integer:\n") )
    y = int( input("integer:\n") )
    z = int( input("integer:\n") )
    print( "="*10 )
    for i in sorted([ x, y, z ]) :
        print( i )

"""
题目6：斐波那契数列。
"""
def exercise6_1() :
    n = int( input("integer:\n") )
    fibList = [0,1]
    def getFib( m, n ) :
        fibList.append(m+n)
        if len( fibList ) == 10 :
            pass
        else :
            getFib( fibList[-1], fibList[-2] )
    getFib( fibList[-1], fibList[-2] )
    print ( fibList )

def exercise6_2() :
    n = int( input("integer:\n") )
    fibList = [0,1]
    for i in range( 2, n ) :
        fibList.append( fibList[-1] + fibList[-2] )
    print ( fibList )


"""
题目7：将一个列表的数据复制到另一个列表中。
"""
def exercise7_1() :
    a = [ 1, 2, 3, 4 ]
    b = a.copy()
    print ( b )

def exercise7_2() :
    a = [ 1, 2, 3, 4 ]
    b = a[:]
    print ( b )

"""
题目8：输出 9*9 乘法口诀表。
"""
def exercise8() :
    for i in range(0,10) :
        s = ""
        for j in range(1,i+1) :
            s += ("%d*%d=%d  " %( j, i, i*j ) )[:7]
        print ( s )

"""
题目9：暂停一秒输出。

"""
def exercise9() :
    import time
    time.sleep(1)
    print( "hehe, sha diao le 1s" )

"""
题目10：暂停一秒输出，并格式化当前时间。
"""
def exercise10() :
    import time
    for i in range(10) :
        print( time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime( time.time() ) ) )
        time.sleep(1)

"""
题目11：古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？
"""
def exercise11_1() :
    monthCnt = int( input( "month:\n" ) )
    def rabbitCnt( month=1, oneMonth=1, twoMonth=0, threeMonth=0 ) :
        if month == monthCnt :
            print ( oneMonth + twoMonth + threeMonth )
        else :
            rabbitCnt( month + 1, twoMonth + threeMonth, oneMonth, twoMonth + threeMonth )
    rabbitCnt() 

def exercise11_2() :
    monthCnt = int( input( "month:\n" ) )
    def rabbitCnt( month=1, oneMonth=1, twoMonth=0 ) :
        if month == monthCnt :
            print ( oneMonth + twoMonth )
        else :
            rabbitCnt( month + 1, twoMonth, oneMonth + twoMonth )
    rabbitCnt()

def exercise11_3() :
    monthCnt = int( input( "month:\n" ) )
    cntList = [ 1, 1 ]
    if monthCnt <= 2 :
        print ( cntList[ monthCnt-1 ] )
    else :
        for i in range( 2, monthCnt ) :
            cntList.append( cntList[-1] + cntList[-2] )
        print ( cntList[ -1 ] )

"""
题目12：判断101-200之间有多少个素数，并输出所有素数。
"""
def exercise12():
    import math
    def primeCheck(i):
        if i%2 ==  0 :
            return False
        check = True
        for j in range(2, int(math.sqrt(i))+1):
            if i % j == 0 :
                check = False
                break
        return check
    primeList = [i for i in range(101, 200) if primeCheck(i)]

    for prime in primeList :
        print ( prime )
    print ( "total count : %d" % len(primeList))
    
"""
题目13：打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。
"""
def exercise13_1():
    forCnt = 0
    for i in range(100, 999) :
        forCnt += 1
        if int(i/100)**3 + int(i%100/10)**3 + int(i%10)**3 == i : #if int(i/100)**3 + int(i/10%10)**3 + int(i%10)**3 == i 
            print ( i )
    print ( "forCnt : %d" %forCnt )

def exercise13_2():
    forCnt = 0
    for i in range(1,10) :
        for j in range(10) :
            for k in range(10) :
                forCnt += 1
                if i**3 + j**3 + k**3 == 100*i+10*j+k :
                    print ( 100*i+10*j+k )
                elif  i**3 + j**3 + k**3 > 100*i+10*j+k :
                    break
    print ( "forCnt : %d" %forCnt )

def exercise13_3():
    forCnt = 0
    for i in range(1,10) :
        breakJ = False
        for j in range(10) :
            if breakJ :
                break
            for k in range(10) :
                forCnt += 1
                if i**3 + j**3 + k**3 == 100*i+10*j+k :
                    print ( 100*i+10*j+k )
                elif  i**3 + j**3 + k**3 > 100*i+10*j+k :
                    if i**3 + j**3 > 100*i+10*j+k :
                        breakJ = True
                    break
    print ( "forCnt : %d" %forCnt )

"""
题目14：将一个正整数分解质因数。例如：输入90,打印出90=2*3*3*5。
"""
def exercise14():
    num = int( input("number:\n") )
    reduceList = list()
    def reduceNum(num):
        for i in range(2, num):
            if num % i == 0 :
                reduceList.append(str(i))
                reduceNum(int(num/i))
                break
        else :
            reduceList.append( str(num) )
    reduceNum(num)
    print ( "%s = " %num + " * ".join(reduceList) )

"""
题目15：利用条件运算符的嵌套来完成此题：学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。
"""
def exercise15():
    score = int(input("score:\n"))
    print ( "A" if score >= 90 else "B" if score >= 60 else "C" )


"""
题目16：输出指定格式的日期。
"""
def exercise16():
    import datetime
    # 输出今日日期，格式为 dd/mm/yyyy。更多选项可以查看 strftime() 方法
    print(datetime.date.today().strftime('%d/%m/%Y'))
    # 创建日期对象
    miyazakiBirthDate = datetime.date(1941, 1, 5)
    print(miyazakiBirthDate.strftime('%d/%m/%Y'))
    # 日期算术运算
    miyazakiBirthNextDay = miyazakiBirthDate + datetime.timedelta(days=1)
    print(miyazakiBirthNextDay.strftime('%d/%m/%Y'))
    # 日期替换
    miyazakiFirstBirthday = miyazakiBirthDate.replace(year=miyazakiBirthDate.year + 1)
    print(miyazakiFirstBirthday.strftime('%d/%m/%Y'))

"""
题目17：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。
"""
def exercise17():
    s = input("inut a string:\n")
    letters = space = digit = others = 0
    for c in s :
        if c.isalpha() :
            letters += 1
        elif c.isspace() :
            space += 1
        elif c.isdigit() :
            digit += 1
        else :
            others += 1
    print ('letters = %d,space = %d,digit = %d,others = %d' % (letters,space,digit,others) )
    
"""
题目18：求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制。
"""
def exercise18():
    num = int(input("number:\n"))
    cnt = int(input("count:\n"))
    numList = list()
    Tn = 0
    for c in range(cnt):
        Tn += num*10**c
        numList.append(Tn)
        print(Tn)
    print( "sum is :%d" %sum(numList) )
        
"""
题目19：一个数如果恰好等于它的因子之和，这个数就称为"完数"。例如6=1＋2＋3.编程找出1000以内的所有完数。
"""
def exercise19():
    for i in range(1, 1000) :
        rList = list()
        for ii in range(1,int(i/2+1)) :
            if i % ii == 0 :
                rList.append(ii)
        if i == sum(rList) :
            print(i)
            print(rList)


"""
题目20：一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？第10次反弹多高？
"""
def exercise20():
    h = 50
    distance = 100
    for i in range(1,10):
        distance += 2*h
        h /= 2
    print("distance :%f" %distance)
    print("10th high:%f" %h )

"""
题目21：猴子吃桃问题：猴子第一天摘下若干个桃子，当即吃了一半，还不瘾，又多吃了一个第二天早上又将剩下的桃子吃掉一半，又多吃了一个。以后每天早上都吃了前一天剩下的一半零一个。到第10天早上想再吃时，见只剩下一个桃子了。求第一天共摘了多少。
"""
def exercise21():
    cnt = 1
    for day in range(9) :
        cnt = (cnt + 1)*2
    print(cnt)

"""
题目22：两个乒乓球队进行比赛，各出三人。甲队为a,b,c三人，乙队为x,y,z三人。已抽签决定比赛名单。有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出三队赛手的名单。
"""
def exercise22_1():
    import itertools
    team1, team2 = 'abc', 'xyz'
    for order1 in itertools.permutations(team1):
        team = [ p+team2[idx] for idx,p in enumerate(order1) ]
        if 'ax' not in team and 'cx' not in team and 'cz' not in team:
            print( team )

def exercise22_2():
    team1, team2 = ['a','b','c'], ['x','y','z']
    def permutations(bl,rl=[]):
        if len(bl) == 1 :
            rl.append(bl[0])
            yield rl
        else :
            for i in bl :
                bbl = bl.copy()
                bbl.remove(i)
                rrl = rl.copy()
                rrl.append(i)
                yield from permutations(bbl, rrl)

    for order1 in permutations(team1):
        team = [ p+team2[idx] for idx,p in enumerate(order1) ]
        if 'ax' not in team and 'cx' not in team and 'cz' not in team:
            print( team )


"""
题目23：打印出如下图案（菱形）
   *
  ***
 *****
*******
 *****
  ***
   *
"""
def exercise23():
    maxLength = int(input("max length:\n"))
    for i in range(maxLength):
        spaceCnt = abs(int(maxLength/2)-i)
        printStr = ' '*spaceCnt + '*'*(maxLength-2*spaceCnt) + ' '*spaceCnt
        print(printStr)
    
"""
题目24：有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13...求出这个数列的前20项之和。
"""
def exercise24():
    a = 2
    b = 1
    s = 0
    for i in range(20):
        s += a/b
        a, b = a+b, a
    print(s)
        
"""
题目25：求1+2!+3!+...+20!的和。
"""
def exercise25_1():
    s = 0
    for i in range(1,21):
        ss = 1
        for ii in range(1,i+1):
            ss *= ii
        s += ss
    print(s)

def exercise25_2():
    t = 1
    s = 0
    for i in range(1,21):
        t *= i
        s += t
    print(s)

"""
题目26：利用递归方法求5!。
"""
def exercise26_1():
    def fact(i, s=1):
        if i <= 1 :
            return s
        else :
            return fact(i-1, i*s)
    print( fact(5) )
        
def exercise26_2():
    def fact(i):
        s = 0
        if i == 0 :
            s = 1
        else :
            s = i * fact(i-1)
        return s
    print( fact(5) )

"""
题目27：利用递归函数调用方式，将所输入的5个字符，以相反顺序打印出来。
"""
def exercise27():
    def output(s):
        if len(s) == 0 :
            return
        else :
            print( s[-1] )
            output(s[:-1])

    s = input("input a string:")
    output(s)

"""
题目28：有5个人坐在一起，问第五个人多少岁？他说比第4个人大2岁。问第4个人岁数，他说比第3个人大2岁。问第三个人，又说比第2人大两岁。问第2个人，说比第一个人大两岁。最后问第一个人，他说是10岁。请问第五个人多大？
"""
def exercise28():
    age = 10
    for i in range(4) :
        age += 2
    print( age )

"""
题目29：给一个不多于5位的正整数，要求：一、求它是几位数，二、逆序打印出各位数字。
"""
def exercise29():
    i = int( input("input an integer:") )
    s = str(i)
    print( "%d位数" %len(s) )
    for ss in s[::-1] :
        print( ss )

"""
题目30：一个5位数，判断它是不是回文数。即12321是回文数，个位与万位相同，十位与千位相同。
"""
def exercise30_1():
    i = int( input("input an integer:") )
    s = str(i)
    isPalindrome = True
    for ii in range( int(len(s)/2) ):
        if s[ii] != s[-ii-1] :
            isPalindrome = False
            break
    print( isPalindrome )

def exercise30_2():
    def checkPalindrome(s):
        if len(s) <= 1 :
            return True
        elif s[0] != s[-1] :
            return False
        else :
            return checkPalindrome(s[1:-1])

    i = int( input("input an integer:") )
    s = str(i)
    print( checkPalindrome(s) )

"""
题目31：请输入星期几的第一个字母来判断一下是星期几，如果第一个字母一样，则继续判断第二个字母。
"""
def exercise31():
    dayMap = {"su":"Sunday", "m":"Monday", "tu":"Tuesday", "w":"Wednesday", "th":"Thursday", "f":"Friday", "sa":"Saturday"}
    letter = input("first letter:").lower()
    if letter in ["s","t"] :
        letter += input("second letter:").lower()
    print ( dayMap[letter] if letter in dayMap else "dada error" )

"""
题目32：按相反的顺序输出列表的值。
"""
def exercise32():
    a = [1,2,3]
    for i in a[::-1] :
        print( i )

"""
题目33：按逗号分隔列表。
"""
def exercise32():
    a = [1,2,3]
    print( ",".join(str(i) for i in a) )

"""
题目34：练习函数调用。
"""
def exercise34():
    def functionTest1( a, *args, **kwargs ):
        print( a )
        print( args )
        print( kwargs )
        print( "-" * 10 )
    def functionTest2( a=1, b=2, c=3):
        print( a )
        print( b )
        print( c )
        print( "-" * 10 )

    functionTest1( 1, 2, 3, x=4, y=5)
    functionTest2( 0, 0 )
    functionTest2( b=0, c=0 )

"""
题目35：文本颜色设置。
"""
def exercise35():
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    print( bcolors.WARNING + "警告的颜色字体?" + bcolors.ENDC )

"""
题目36：求100之内的素数。
"""
def exercise36():
    import math
    def primeCheck(i):
        if i%2 ==  0 :
            return False
        check = True
        for j in range(2, int(math.sqrt(i))+1):
            if i % j == 0 :
                check = False
                break
        return check
    for i in range(100) :
        if primeCheck(i) :
            print(i)


"""
题目37：对10个数进行排序。
"""
def exercise37_1():
    l = input("输入若干数字，以空格分隔：")
    intList = [int(i) for i in l.split(" ")]
    intList.sort()
    print( " ".join([str(i) for i in intList]) )

def exercise37_2():
    l = input("输入若干数字，以空格分隔：")
    intList = sorted( [int(i) for i in l.split(" ")] )
    print( " ".join([str(i) for i in intList]) )

"""
题目38：求一个n*n随机矩阵主对角线元素之和。
"""
def exercise38():
    import random
    n = int(input("n:"))
    matrix = [ [random.randint(0,100) for i in range(n)] for j in range(n) ]
    for l in matrix :
        print ( l )
    print( sum( matrix[i][i] for i in range(n) ) )

"""
题目39：有一个已经排好序的数组。现输入一个数，要求按原来的规律将它插入数组中。
"""
def exercise39():
    l = input("输入若干排序好的整数，以空格分隔：")
    i = int(input("输入插入其中的整数："))
    intList = [int(i) for i in l.split(" ")]
    if i <= intList[0] :
        rstList = [i] + intList
    elif i >= intList[-1] :
        rstList = intList + [i]
    else :
        for idx in range(len(intList)-1) :
            if intList[idx] <= i < intList[idx+1] :
                rstList = intList[:idx+1] + [i] + intList[idx+1:]
                break
    print( " ".join([str(i) for i in rstList]) )

"""
题目40：将一个数组逆序输出。
"""
def exercise40():
    l = [ 1, 2, 3, 4, 5, 6 ]
    print(l[::-1])

"""
通过方法名运行方法，默认运行最后一个exercise
"""
def runMethod(exerciseName=None):
    if exerciseName :
        exerciseName = "exercise" + exerciseName
    else :
        lastExercise = sorted( [ int( name.replace("exercise", "").split("_")[0] ) for name in globals().keys() if "exercise" in name ] )[-1]
        defList = [name for name in globals().keys() if "exercise%d"%lastExercise in name]
        lastDef = "_%d" %( sorted( [ int(_def.split("_")[1]) for _def in defList ] )[-1] ) if "_" in defList[0] else ""
        exerciseName = "exercise%d%s" %(lastExercise, lastDef)
    print( "run %s" %exerciseName )
    globals()[ exerciseName ]()

if __name__ == "__main__" :
    runMethod()
