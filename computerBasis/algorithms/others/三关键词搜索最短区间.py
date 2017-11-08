A=[1,25,30,45,50,62,55,75]
B=[2,3,14,15,19,31,47,51]
C=[6,7,20,38,40,53,60,61]

global minLength,a,b,c
minLength = 20

def getMin(goalList):
    global minLength,a,b,c
    if goalList[0] == min(A[0],B[0],C[0]):
        L = max(A[0],B[0],C[0]) - min(A[0],B[0],C[0])
        if minLength > L:
            minLength, a, b, c= L, A[0], B[0], C[0]
        goalList.pop(0)
        return True
    else : return False

while A and B and C:
    for goalList in [A,B,C]:
        is_min = getMin(goalList)
        if is_min:
            break

print minLength
print 'A=',a,'B=',b,'C=',c
