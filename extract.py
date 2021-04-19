import re

def getTransposonPos(f):
    for x in f:
        res = x.split()
    return (res[5],res[6])

def getSequence(fasta,start,end):
    seq = ""
    for x in fasta:
        res = x.split()
    for x in range(start,end):
        seq += (res[0][x])
    return (seq)

def getRightFlankPos(fasta):
    res = fasta.readline()
    res = res.split()
        #^.+[|(](\d+)[.]+(\d+)
    print(res)


print("hello world")
f = open("both500.fa.out")
fasta = open("both500.fa.out_both500_flank_500.fasta")

getRightFlankPos(fasta)

location = getTransposonPos(f)
start = int(location[0])
end = int(location[1])

transposon = getSequence(fasta,start,end)
print(transposon)

length = int(end) - int(start)

print(length)