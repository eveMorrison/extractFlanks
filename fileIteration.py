import re

repMaskFile = open("test.fa.out", "r")

for line in repMaskFile:
   if re.search('^.+\d',line,0):
      values = line.split()
      id = values[14]
      te_start = values[5]
      te_end = values[6]


linelist = repMaskFile.readlines()
fileLeng = len(linelist)
 
repMaskFile.close()