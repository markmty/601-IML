import sys, math, csv

file_Name = sys.argv[1]

fd=open(file_Name)
data=fd.read()
raw_list=data.split("\n")
raw_list.pop()
fd.close()

first_line=raw_list[0]
first_list=first_line.split(",")
key=first_list[len(first_list)-1]

if key=="grade\r":
   pos="A\r"
   neg="notA\r"
else:
   pos="yes"
   neg="no"

num1=0
num2=0
raw_list.pop(0)
stat=raw_list


for element in stat:
    list=element.split(",")
    if list[len(list)-1]==pos:
       num1+=1
    else:
       num2+=1


num1=float(num1)
num2=float(num2)


prob_1=num1/(num1+num2)
prob_2=num2/(num1+num2)
entropy=prob_1 * math.log((1/prob_1),2) + prob_2 * math.log((1/prob_2),2)
print "entropy:",round(entropy,3)

if num1>num2 :
   print "error:",round(prob_2,2)
else:
   print "error:",round(prob_1,2)







