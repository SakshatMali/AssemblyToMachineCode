#------------------------- ASSEMBLER -------------------------

#------------------------- OPCODES -------------------------
dict = {

"CLA"   :	"0000" ,
"LAC"	:	"0001" ,
"SAC"	:	"0010" ,
"ADD"	:	"0011" ,
"SUB"	:	"0100" ,
"BRZ"	:	"0101" ,
"BRN"	:	"0110" ,
"BRP"	:	"0111" ,
"INP"	:	"1000" ,
"DSP"	:	"1001" ,
"MUL"	:	"1010" ,
"DIV"	:	"1011" ,
"STP"	:	"1100" 

}

def checkInD(s):
    if s in dict:
        return True

    else:
        return False

def checkO(s):
    if s=="CLA" or s=="STP":
        return True
    else:
        return False

def checkI(s):
    if s=="INP" or s=="SAC":
        return True
    else:
        return False

def checkB(s):
    if s=="BRZ" or s=="BRN" or s=="BRP":
        return True
    else:
        return False

def check(s):
    if s=="START" or s=="END":
        return True
    else:
        return False

opcode=[]
symbol=[]
operands=[]
literal=[]
adss=[]
val=[]
adres_l=[]
sym_co=[]
SE=["@","@"]

#------------------------- Creating Virtual Adresses for Referencing -------------------------

def DecToBin(a):
    #a = int(input())
    s=""
    if a==0:
        return "00000000"
    else:    
        while a>1:
            b=a/2
            c=a%2
            s+=str(c)
            a=int(b)

        m =("1"+s[::-1])

    if len(m)<8:
        z="00000000"

        k=z[len(m):]+ m

        return k
    else:
        return m


#------------------------- 1st PASS -------------------------

#------------------------- Reading txt Files & Creating Tables -------------------------

file = open("set.txt", "r")
l_c=0
for c in file:
    l = [str(x) for x in c.split()]
    n = len(l)
    for i in range(n):
        if l[0][0:2]=="//":
            break
        elif check(l[0]):
            if l[0]=="START":
                SE[0]="START"
            if l[0]=="END":
                SE[1]="END"
            if n!=1:
                l_c+=int(l[1])
            break
        elif l[i][-1]==":":
            symbol.append(l[i][0:-1])
            sym_co.append(l_c)
            adss.append(l[i][0:-1])
        else:
            opcode.append(l[i])
            li = []
            lo = []
            if l[n-1]==l[i]:
                li.append("@")
                lo.append("@")
            elif checkI(l[i]):
                for g in range(i+1,n):
                    try:
                        x = int(l[g])
                        li.append(l[g])
                        adss.append(l[g])
                        adres_l.append(l[g])
                        lo.append("@")
                    except ValueError:
                        lo.append(l[g])
                        adss.append(l[g])
                        val.append(l[g]) 
                        li.append("@")
            else:
                for j in range(i+1,n):
                    if l[j][0]=="=":
                        b = l[j][1:]
                        try:
                            x = int(b)
                            li.append(b)
                            adss.append(b)
                            lo.append("@")
                        except ValueError:
                            lo.append(b)
                            adss.append(b) 
                            li.append("@")
                    else:
                        try:
                            x = int(l[j])
                            li.append(l[j])
                            adss.append(l[j])
                            adres_l.append(l[j])
                            lo.append("@")
                        except ValueError:
                            lo.append(l[j])
                            adss.append(l[j]) 
                            li.append("@")
            literal.append(li)
            operands.append(lo)
            break
    l_c+=1


print("-------------------------SYMBOL TABLE-------------------------")
print (symbol)

print("-------------------------LITERAL TABLE-------------------------")
print (literal)

print ("-------------------------OPERAND TABLE-------------------------")
print (operands)

print ("-------------------------OPCODE TABLE-------------------------")
print (opcode) 


# To get the list of the defined Variables
K = set(adss)
P = sorted(list(K))



#------------------------- 2nd PASS -------------------------


#------------------------- Writing Maching Code in txt File & Finding Errors -------------------------

file_n = open('go.txt','w')

if SE[0] != "START":
    file_n.write("Error: Cannot Execute as START is missing in the Start of Code")
elif SE[1] != "END":
    file_n.write("Error: Cannot Execute as END is missing in the End of Code")
else:
    for k in range(len(opcode)):

        if len(symbol)!= len(set(symbol)):
            file_n.write("Error: Same label defined more than once")
            break

        else:
            m=opcode[k]

            if checkInD(m):
                t=dict[m]
                if checkO(m):
                    if len(operands[k])==1 and len(literal[k])==1 and literal[k][0]=="@" and operands[k][0]=="@":
                        if m == "CLA":
                            t+=DecToBin(0)
                            file_n.write(t+'\n')
                        else:
                            t+=DecToBin(255)
                            file_n.write(t+'\n')
                    else:
                        file_n.write("Error: "+m+" cannot take any operands" + '\n')

                elif checkB(m):
                    if len(operands[k])==1 and operands[k][0] in symbol:
                        h = symbol.index(operands[k][0])
                        t+=DecToBin(sym_co[h])
                        file_n.write(t+'\n')
                    else:
                        file_n.write("Error: Symbol not defined"+'\n')

                else:
                    if len(operands[k])!=1:
                        file_n.write("Error: Number of operands are not correct"+'\n')
                    elif len(operands[k])==1:
                        if m=="DIV" and literal[k][0]=="0":
                            file_n.write("Error: Division by 0"+'\n')
                        elif checkInD(operands[k][0]):
                            file_n.write("Error: This Variable cannot be used"+'\n')
                        elif operands[k][0]=="@" and literal[k][0]=="@":
                            file_n.write("Error: No operand is present"+'\n')
                        elif operands[k][0] not in val and literal[k][0]=="@":
                            file_n.write("Error: Variable is not Defined"+'\n')
                        else:
                            if (operands[k][0]=="@"):
                                h = P.index(literal[k][0])
                                if literal[k][0] in adres_l and int(literal[k][0])>255:
                                    file_n.write("Error: Address has more than 8 bits"+'\n')
                                elif literal[k][0] in adres_l:
                                    t+=DecToBin(int(literal[k][0]))
                                    file_n.write(t+'\n')
                                else:
                                    t+=DecToBin(len(opcode)+10+h)
                                    file_n.write(t+'\n')
                            else:
                                h = P.index(operands[k][0])
                                t+=DecToBin(len(opcode)+10+h)
                                file_n.write(t+'\n')
            else:
                file_n.write("Error: Wrong Opcode or the Label is Invalid"+'\n')