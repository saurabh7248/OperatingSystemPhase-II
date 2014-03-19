from copy import deepcopy
from random import *
num=['0','1','2','3','4','5','6','7','8','9']
SI=3
TI=0
PI=0
R=[' ',' ',' ',' ']
IC=[' ',' ']
IR=[' ',' ',' ',' ']
M=[]
PTR=[' ',' ',' ',' ']
PID=0
TTC=0
LLC=0
TTL=0
TLL=0
EM=0
ptr=0
for a in range(0,300):
    M.append(deepcopy(R))
inputfile=open(r'E:\osinputm1.txt','r')
output=open(r'E:\output.txt','w')
C=False
###################################################
def AllocatePage(PageNumber):
    global M,PTR
    previousaddresses=[int(PTR[2]+PTR[3])]
    for count in range(int(PTR[2]+PTR[3]),int(PTR[2]+PTR[3])+10):
        if (M[count][0]==" "):
            break
        else:
            previousaddresses.append(int(M[count][2]+M[count][3]))
    while(True):
        a=randint(0,29)
        if(a not in previousaddresses):
            M[int(PTR[2]+PTR[3])*10+PageNumber][0]="1"
            M[int(PTR[2]+PTR[3])*10+PageNumber][1]="0"
            M[int(PTR[2]+PTR[3])*10+PageNumber][2]=str(int(a/10))
            M[int(PTR[2]+PTR[3])*10+PageNumber][3]=str(int(a%10))
            break
    return int(M[int(PTR[2]+PTR[3])*10+PageNumber][2]+M[int(PTR[2]+PTR[3])*10+PageNumber][3])
###################################################
def LoadInstruction(location):
    global M,PTR
    ptr=int(PTR[2]+PTR[3])
    index=int(location/10)
    digit1=M[ptr*10+index][2]
    digit2=M[ptr*10+index][3]
    return deepcopy(M[int(digit1+digit2)*10+(location%10)])
###################################################
def MOS():
    global PI,TI,IC,IR,SI,R,M
    if(PI==0):
        if(TI==0 and SI==1):
            READ()
        elif(TI==0 and SI==2):
            WRITE()
        elif(TI==0 and SI==3):
            TERMINATE([0])
        elif(TI==2 and SI==0):
            TERMINATE([3])
        elif(TI==2 and SI==1):
            TERMINATE([3])
        elif(TI==2 and SI==2):
            WRITE()
            TERMINATE([3])
        elif(TI==2 and SI==3):
            TERMINATE([3])
    else:
        if(TI==0 and PI==1):
            TERMINATE([4])
        elif(TI==0 and PI==2):
            TERMINATE([5])
        elif(TI==0 and PI==3):
            if((IR[0]=="G" and IR[1]=="D")or(IR[0]=="S" and IR[1]=="R")):
                IC=int(IC[0]+IC[1])
                IC-=1
                if(IC<10):
                    IC='0'+str(IC)
                else:
                    IC=str(IC)
                IC=list(IC)
                AllocatePage(int(IR[2]))
                PI=0
            else:
                TERMINATE([6])
        elif(TI==2 and PI==1):
            TERMINATE([3,4])
        elif(TI==2 and PI==2):
            TERMINATE([3,5])
        elif(TI==2 and PI==3):
            TERMINATE([3])
def WRITE():
    global IR,LLC,M,PTR,LLC,TLL
    LLC+=1
    if(LLC>TLL):
        TERMINATE([2])
    IR[3]='0'
    block=int(M[int(PTR[2]+PTR[3])*10+int(IR[2])][2]+M[int(PTR[2]+PTR[3])*10+int(IR[2])][3])
    block*=10
    for x in range(block,block+10):
        for y in range(0,4):
            output.write(M[x][y])
    output.write('\n')
def TERMINATE(ErrorCodes):
    global PID,PI,TI,SI,IC,PID,IR,TTL,TTC,TLL,LLC
    output.write("IC:"+str(IC)+"    PID:"+str(PID)+"      IR:"+str(IR)+"   TTL:"+str(TTL)+"   TTC:"+str(TTC)+"   TLL:"+str(TLL)+"   LLC:"+str(LLC)+"\n")
    for count in range(0,len(ErrorCodes)):
        code=ErrorCodes[count]
        if(code==0):
            output.write("No Error\n")
        elif(code==1):
            output.write("Out of Data\n")
        elif(code==2):
            output.write("Line Limit Exceeded\n")
        elif(code==3):
            output.write("Time Limit Exceeded\n")
        elif(code==4):
            output.write("Operation Code Error\n")
        elif(code==5):
            output.write("Operand Code Error\n")
        elif(code==6):
            output.write("Invalid Page Fault\n")
    output.write('\n\n')
    LOAD()
def READ():
    global M,IR
    IR[3]='0'
    block=int(M[int(PTR[2]+PTR[3])*10+int(IR[2])][2]+M[int(PTR[2]+PTR[3])*10+int(IR[2])][3])
    block*=10
    datacard=inputfile.readline()
    if(datacard.endswith('\n')):
        datacard=datacard[0:len(datacard)-1]
    if(datacard.startswith('$END')):
        TERMINATE([1])
    else:
        for count in range(len(datacard),40):
            datacard+=' '
        datacard=list(datacard)
        for count in range(0,10):
            M[block]=deepcopy(datacard[4*count:4*count+4])
            block+=1
def EXECUTEUSERPROGRAM():
    global IC,SI,IR,M,PI,R,TTC,TTL,TI,C,M
    cmos=False
    ote=False
    while(True):
        IC=int(IC[0]+IC[1])
        IR=LoadInstruction(IC)
        if(IC==10):
            print(IC)
        IC+=1
        if(IC<10):
            IC='0'+str(IC)
        else:
            IC=str(IC)
        IC=list(IC)
        if(((IR[2] in num) and (IR[3] in num)) or(IR[0]=='H')):
            if(IR[0]+IR[1]=='LR'):
                SI=0
                R=deepcopy(M[int(IR[2]+IR[3])])
                index=int(IR[2]+IR[3])
                index=(int(PTR[2]+PTR[3])*10)+int(index/10)
                if(M[index][0]=="1"):
                    R=deepcopy(M[int(M[index][2]+M[index][3])*10+int(IR[3])])
                    print(R)
                else:
                    PI=3
                    MOS()
            elif(IR[0]+IR[1]=='SR'):
                SI=0
                index=int(IR[2]+IR[3])
                index=(int(PTR[2]+PTR[3])*10)+int(index/10)
                if(M[index][0]=="1"):
                    M[int(M[index][2]+M[index][3])*10+int(IR[3])]=deepcopy(R)
                else:
                    PI=3
                    MOS()
                    TTC-=1
            elif(IR[0]+IR[1]=='CR'):
                SI=0
                index=int(IR[2]+IR[3])
                index=(int(PTR[2]+PTR[3])*10)+int(index/10)
                if(M[index][0]=="1"):
                    if(R==M[int(M[index][2]+M[index][3])*10+int(IR[3])]):
                        C=True
                    else:
                        C=False
                else:
                    PI=3
                    MOS()
            elif(IR[0]+IR[1]=='BT'):
                SI=0
                if(C):
                    IC=int(IR[2]+IR[3])
                    if(IC<10):
                        IC='0'+str(IC)
                    else:
                        IC=str(IC)
                    IC=list(IC)
            elif(IR[0]+IR[1]=='GD'):
                index=int(IR[2]+IR[3])
                index=(int(PTR[2]+PTR[3])*10)+int(index/10)
                if(M[index][0]=="1"):
                    SI=1
                    MOS()
                else:
                    PI=3
                    MOS()
                    TTC-=1
            elif(IR[0]+IR[1]=='PD'):
                index=int(IR[2]+IR[3])
                index=(int(PTR[2]+PTR[3])*10)+int(index/10)
                if(M[index][0]=="1"):
                    SI=2
                    MOS()
                else:
                    PI=3
                    MOS()
            elif(IR[0]=='H'):
                SI=3
                cmos=True
            else:
                PI=1
                cmos=True
        else:
            PI=2
            cmos=True
        TTC+=1
        if(TTC==TTL):
            TI=2
            MOS()
        if(cmos):
            MOS()
            cmos=False
def STARTEXECUTION():
    global IC
    IC=['0','0']
    EXECUTEUSERPROGRAM()
def LOAD():
    global M,TTL,LLC,TTC,TLL,PTR,PI,TI,PID
    M=[]
    bno=0
    for a in range(0,300):
        M.append([' ',' ',' ',' '])
    pointer=0
    inputfeed=inputfile.readline()
    while(inputfeed):
        if(inputfeed.endswith('\n')):
            inputfeed=inputfeed[0:len(inputfeed)-1]
        if(inputfeed.startswith("$AMJ") or inputfeed.startswith("$DTA") or inputfeed.startswith("$END")):
            if(inputfeed.startswith("$AMJ")):
                M=[]
                for a in range(0,300):
                    M.append([' ',' ',' ',' '])
                PID=int(inputfeed[4:8])
                TTL=int(inputfeed[8:12])
                TLL=int(inputfeed[12:16])
                LLC=0
                TTC=0
                TI=0
                PI=0
                pointer=0
                ptr=randint(0,29)
                PTR[0]='0'
                PTR[1]='0'
                PTR[2]=str(int(ptr/10))
                PTR[3]=str(ptr%10)
                bno=0
            if(inputfeed.startswith("$END")):
                pass
            if(inputfeed=='$DTA'):
                STARTEXECUTION()
        else:
            for count in range(len(inputfeed),40):
                    inputfeed+=' '
            inputfeed=list(inputfeed)
            index=AllocatePage(bno)
            index=index*10
            for count in range(0,10):
                M[index]=deepcopy(inputfeed[4*count:4*count+4])
                index+=1
            bno+=1
        inputfeed=inputfile.readline()
    if(not inputfeed):
        inputfile.close()
        output.close()
        exit(0)
LOAD()
