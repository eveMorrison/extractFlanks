repMaskFile = open("test.fa.out", "r")

linelist = repMaskFile.readlines()
fileLeng = len(linelist)

i = 3
while(i<fileLeng):
   values = linelist[i].split()
   print('ID: ',values[14], '\nTransposon Start: ', values[5], '\nTransposon End: ', values[6] )
   i+=1
 
repMaskFile.close()