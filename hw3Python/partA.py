import sys, math

fd1=open("9Cat-Train.labeled")
tr_data=fd1.read()
list1=tr_data.split('\n') #list of each line
list1.pop(len(list1)-1)
fd1.close()

fd2=open("9Cat-Dev.labeled")
cmp_data=fd2.read()
list4=cmp_data.split('\n')
list4.pop(len(list4)-1)
fd2.close()

fd3=open(sys.argv[1])
input_data=fd3.read()
list7=input_data.split('\n')
list7.pop(len(list7)-1)
fd3.close


attr=["Gender","Age","Student?","PreviouslyDeclined?","HairLength",
      "Employed?","TypeOfColateral","FirstLoan","LifeInsurance","Risk"]

print 2**9
print int(math.ceil((2**9)*0.3)+1)
print 3**9+1

def validfeatures(listof20):
    for element in attr:
        listof20.remove(element)
    return listof20

def initialhypothesis(lists):

    for string in lists:
        helplist1=string.split()
        if (helplist1[19]=="high"):
           break

    return validfeatures(helplist1)

def update(orig,new):
    for i in xrange(9):
        if (orig[i]!=new[i]):
           orig[i]="?"

    return orig

def writeFile(filename,contents, mode="wt"):
    with open(filename,mode) as fout:
         fout.write(contents)

def riskoutofhypo(hypo,truth):
    for i in xrange(9):
        if (hypo[i]!="?") and (hypo[i]!=truth[i]):
            return "low"

    return "high"


def misclassification(final_hypo):
    miss=0
    for string in list4:
        list5=string.split()
        list6=validfeatures(list5)
        risk=riskoutofhypo(final_hypo,list6)
        if (risk!=list6[9]):
           miss += 1

    return float(miss)/len(list4)

def judgeInput(final_hypo):
    for string in list7:
        list8=string.split()
        list9=validfeatures(list8)
        risk=riskoutofhypo(final_hypo,list9)
        print risk



def training(init_hypo,lists):
    i=0
    contents=""
    for string in lists:
        i+=1
        list2=string.split()
        list3=validfeatures(list2)
        if (list3[9]=="high"):
            update(init_hypo,list3)

        if ((i%30)==0):
           target=init_hypo[:-1]
           contents+="\t".join(target)+"\n"
          
    writeFile("partA4.txt",contents)

    print misclassification(init_hypo)
    judgeInput(init_hypo)


training(initialhypothesis(list1),list1)

