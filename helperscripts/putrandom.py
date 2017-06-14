import random

fs=open('data','r')
fr=open('result','w')

for i in fs.readlines():
    fr.write(i[0:-1]+ ' '+str(random.random())+'\n')