import re

def getTransposonPos(f):
    for x in f:
        res = x.split()
    return (res[5],res[6])

def getSequence(start,end):
    fasta = open("both500.fa.out_both500_flank_500.fasta")
    seq = ""
    for x in fasta:
        res = x.split()
    for x in range(start,end):
        seq += (res[0][x])
    fasta.close()
    return (seq)

def getSequence1(start,end):
    fasta = open("both500.fa.out_both500_flank_500.fasta")
    seq = ""
    for x in fasta:
        txt = x
        txt = txt.split()
    for x in range(start,end):
        seq = seq + (txt[0][x])
    fasta.close()
    return (seq)

def getFlankPos():
    fasta = open("both500.fa.out_both500_flank_500.fasta")
    txt = fasta.readline()
    txt = txt.split()
    num = re.search('^.+[|(](\d+)[.]+(\d+)',txt[0],0)
    flankBegin = int(num.group(1))
    flankEnd = int(num.group(2))
    fasta.close()
    return(flankBegin,flankEnd)


f = open("both500.fa.out")


flankPos = getFlankPos()
leftFlankStart = int(flankPos[0])
rightFlankEnd = int(flankPos[1])

location = getTransposonPos(f)
leftFlankEnd = int(location[0])
rightFlankStart = int(location[1])

transposon = getSequence(leftFlankEnd,rightFlankStart)
print(transposon)
flankLeft = getSequence(leftFlankStart,leftFlankEnd)
print(flankLeft)
flankRight = getSequence(rightFlankStart,rightFlankEnd )
print(flankRight)
