import sys, math, csv

train_name=sys.argv[1]
test_name=sys.argv[2]

fd1=open(train_name)
train_data=fd1.read()
train_list=train_data.split("\n")
train_list.pop()
fd1.close

fd2=open(test_name)
test_data=fd2.read()
test_list=test_data.split("\n")
test_list.pop()
fd2.close

def key(content):
    attr_n_key=content[0]
    list1=attr_n_key.split(",")
    return list1[len(list1)-1]

def attr(content):
    attr_n_key=content[0]
    list1=attr_n_key.split(",")
    list1.pop()
    return list1

#print key(train_list)
#print attr(train_list)

def statistic(content):
    statistics=[]
    content.pop(0)
    for string in content:
        node=string.split(",")
        statistics.append(node)
    return statistics

def key_statistics(stat):
    #print statistics
    key_stat={}
    key_stat[pos]=0
    key_stat[neg]=0
    for element in stat:
        label=element[len(element)-1]
            #if label not in key_stat:
            #key_stat[label]=0
        key_stat[label]+=1
    #print key_stat
    return key_stat

def entropy(num1,num2):
    if num1==0 or num2==0:
       result=float(0)
    else:
       num1=float(num1)
       num2=float(num2)
       prob1=num1/(num1+num2)
       prob2=num2/(num1+num2)
       result=prob1*math.log((1/prob1),2)+prob2*math.log((1/prob2),2)
    return result

def cond_etrp(num1,num2,ind,stats):
    stat1=[]
    stat0=[]
    temp_list=[]
    
    for element in stats:
        if element[ind] not in temp_list:
           temp_list.append(element[ind])

    for element in stats:
        if element[ind]==temp_list[0]:
           stat0.append(element)
        else:
           stat1.append(element)
    key_stat0=key_statistics(stat0)
    key_stat1=key_statistics(stat1)
    values0=key_stat0.values()
    values1=key_stat1.values()

    v1=values0[0]
    v2=values0[1]
    v3=values1[0]
    v4=values1[1]
    sum1=float(v1+v2)
    sum2=float(v3+v4)
    sum=sum1+sum2
    prob1=sum1/sum
    prob2=sum2/sum

    return prob1*entropy(v1,v2)+prob2*entropy(v3,v4)

def split(stat,ind):
    temp_list=[]
    for element in stat:
        if element[ind] not in temp_list:
           temp_list.append(element[ind])

    stat1=[]
    stat0=[]
    for element in stat:
        if element[ind]==temp_list[0]:
           stat0.append(element)
        else:
           stat1.append(element)
    return [stat0,stat1]

def split_attr_values(stat,ind):
    temp_list=[]
    for element in stat:
        if element[ind] not in temp_list:
           temp_list.append(element[ind])
    return temp_list

def float_min(list):
    temp=1
    for num in list:
        if num<temp:
           temp=num
    return temp

def find_min(list):
    temp=len(stat)
    for num in list:
        if num<temp:
           temp=num
    return temp

def rule(dict):
    values=dict.values()
    if key_name=="grade\r":
       values.reverse()
    min=find_min(values)
    i=values.index(min)
    
    if i==0:
       return neg
    else:
       return pos

def countmistake(stat,rule):
    count=0
    for element in stat:
        if element[len(element)-1] != rule:
           count += 1
    return count

def filter(stat,attr_ind,attr_value):
    temp=[]
    for element in stat:
        if element[attr_ind]==attr_value:
           temp.append(element)
    return temp

key_name=key(train_list)
if (key_name=="grade\r"):
   pos="A\r"
   neg="notA\r"
else:
   pos="yes"
   neg="no"

attr_name=attr(train_list)
stat=statistic(train_list)
key_stat=key_statistics(stat)
values=key_stat.values()
if (key_name=="grade\r"):
   values.reverse()
#print entropy(values[0],values[1])
cond_etrps=[]
for i in xrange(len(attr_name)):
    cond_etrps.append(cond_etrp(values[0],values[1],i,stat))
min=min(cond_etrps)
#print min
if (entropy(values[0],values[1])-min)>0.1:
    #print (entropy(values[0],values[1])-min)
   split_at=cond_etrps.index(min)
   attr_values=split_attr_values(stat,split_at)
   left=split(stat,split_at)[0]
   right=split(stat,split_at)[1]

   key_stat_l=key_statistics(left)
#print key_stat_l
   values_l=key_stat_l.values()
   if (key_name=="grade\r"):
      values_l.reverse()
   cond_etrps_l=[]
   for i in xrange(len(attr_name)):
       cond_etrps_l.append(cond_etrp(values_l[0],values_l[1],i,left))
   min_l=float_min(cond_etrps_l)
   split_at_l= -1
   if (entropy(values_l[0],values_l[1])-min_l)>0.1:
       split_at_l=cond_etrps_l.index(min_l)
       attr_values_l=split_attr_values(left,split_at_l)
       ll=split(left,split_at_l)[0]
       lr=split(left,split_at_l)[1]

   key_stat_r=key_statistics(right)
   values_r=key_stat_r.values()
   if (key_name=="grade\r"):
       values_r.reverse()
   cond_etrps_r=[]
   for i in xrange(len(attr_name)):
       cond_etrps_r.append(cond_etrp(values_r[0],values_r[1],i,right))
   min_r=float_min(cond_etrps_r)
   split_at_r= -1
   if (entropy(values_r[0],values_r[1])-min_r)>0.1:
       split_at_r=cond_etrps_r.index(min_r)
       attr_values_r=split_attr_values(right,split_at_r)
       rl=split(right,split_at_r)[0]
       rr=split(right,split_at_r)[1]

#print key_stat
#print attr_name[split_at]
#print attr_values
#print key_statistics(left)
#print key_statistics(right)

#if split_at_l != -1 :
#print attr_name[split_at_l]
#  print attr_values_l
#  print key_statistics(ll)
#  print key_statistics(lr)

#if split_at_r != -1 :
#  print attr_name[split_at_r]
#  print attr_values_r
#  print key_statistics(rl)
#  print key_statistics(rr)

orig_key=values
attr_1st=attr_name[split_at]
key_l=values_l
key_r=values_r
error_l=find_min(key_l)
error_r=find_min(key_r)
rule_l=rule(key_statistics(left))
rule_r=rule(key_statistics(right))

if split_at_l != -1 :
   attr_2nd=attr_name[split_at_l]
   key_ll=key_statistics(ll).values()
   key_lr=key_statistics(lr).values()
   if (key_name=="grade\r"):
       key_ll.reverse()
       key_lr.reverse()
   error_ll=find_min(key_ll)
   error_lr=find_min(key_lr)
   error_l=error_ll+error_lr
   rule_ll=rule(key_statistics(ll))
   rule_lr=rule(key_statistics(lr))

if split_at_r != -1 :
   attr_3rd=attr_name[split_at_r]
   key_rl=key_statistics(rl).values()
   key_rr=key_statistics(rr).values()
   if (key_name=="grade\r"):
       key_rl.reverse()
       key_rr.reverse()
   error_rl=find_min(key_rl)
   error_rr=find_min(key_rr)
   error_r=error_rl+error_rr
   rule_rl=rule(key_statistics(rl))
   rule_rr=rule(key_statistics(rr))

error_train=float(error_l+error_r)/float(len(stat))
error_train=round(error_train,2)

test_stat=statistic(test_list)
test_l=filter(test_stat,split_at,attr_values[0])
test_r=filter(test_stat,split_at,attr_values[1])
sum3=countmistake(test_l,rule_l)+countmistake(test_r,rule_r)
#print countmistake(test_l,rule_l)
#print countmistake(test_r,rule_r)

if split_at_l != -1:
   test_ll=filter(test_l,split_at_l,attr_values_l[0])
   test_lr=filter(test_l,split_at_l,attr_values_l[1])
   sum3 += countmistake(test_ll,rule_ll)
   sum3 += countmistake(test_lr,rule_lr)
   sum3 -= countmistake(test_l,rule_l)

if split_at_r != -1:
   test_rl=filter(test_r,split_at_r,attr_values_r[0])
   test_rr=filter(test_r,split_at_r,attr_values_r[1])
   sum3 += countmistake(test_rl,rule_rl)
   sum3 += countmistake(test_rr,rule_rr)
   sum3 -= countmistake(test_r,rule_r)
   #print countmistake(test_rl,rule_rl)
   #print countmistake(test_rr,rule_rr)

error_test=float(sum3)/float(len(test_stat))
error_test=round(error_test,2)

#print sum3
#print test_l
#print test_r
#print test_ll
#print test_lr
#print test_rl
#print test_rr
#print rule_ll
#print rule_lr
#print rule_rl
#print rule_rr


print "["+str(orig_key[0])+"+/"+str(orig_key[1])+"-]"
print attr_1st+" = "+str(attr_values[0])+": ["+str(key_l[0])+"+/"+str(key_l[1])+"-]"

if split_at_l != -1:
   print "| "+attr_2nd+" = "+attr_values_l[0]+": ["+str(key_ll[0])+"+/"+str(key_ll[1])+"-]"
   print "| "+attr_2nd+" = "+attr_values_l[1]+": ["+str(key_lr[0])+"+/"+str(key_lr[1])+"-]"

print attr_1st+" = "+str(attr_values[1])+": ["+str(key_r[0])+"+/"+str(key_r[1])+"-]"

if split_at_r != -1:
   print "| "+attr_3rd+" = "+attr_values_r[0]+": ["+str(key_rl[0])+"+/"+str(key_rl[1])+"-]"
   print "| "+attr_3rd+" = "+attr_values_r[1]+": ["+str(key_rr[0])+"+/"+str(key_rr[1])+"-]"

print "error(train): "+str(error_train)
print "error(test): "+str(error_test)


