import sys

#question1
print 2**4
#question2
print 2**(2**4)

#training file open
fd1=open("4Cat-Train.labeled")
train_data=fd1.read()
train_list=train_data.split("\n")
train_list.pop()
fd1.close()

#testing file open
fd2=open(sys.argv[1])
test_data=fd2.read()
test_list=test_data.split("\n")
test_list.pop()
fd2.close()

#initialize hypothesis
G=["?","?","?","?"]
S=["Null","Null","Null","Null"]

attr=["Gender","Age","Student?","PreviouslyDeclined?","Risk"]

def validfeatures(listof10):
    for element in attr:
        listof10.remove(element)
    return listof10

def checkinclude(hypo,train):
    outcome=TRUE
    for i in xrange(4)
        if (hypo[i]!="?") and (hypo[i]!=train[i]):
           outcome=False
           break

    return outcome

def mingeneral(s,d):
    for i in xrange(4):
        if (s[i]=="Null"):
            s[i]=d[i]
        elif (S[index][i]!="?") and (s[i]!=d[i]):
            s[i]="?"
        else:
            continue

def minspecific(g,d,s):
    for i in xrange(4):
        if (s[i]!=d[i]) and (s[i]!="?"):
            if (g[i]=="?"):
                temp=g[:]
                temp[i]=s[i]
                G.append(temp)

    for hypo in G:
        if checkinclude(hypo,d):
           G.remove(hypo)

    G=list(set(G))

def train():
    for string in train_list
        list1=string.split()
        list2=validfeatures(list1)
        if (list2[4]=="high"):
            list2.pop()
            #list2 is the training instance
            for hypo in G:
                if (not checkinclude(hypo,list2)):
                    G.remove(hypo)
            for hypo in S:
                mingeneral(hypo,list2)

        else:
            list2.pop()
            for hypo in S:
                if (checkinclude(hypo,list2)):
                    S.remove(hypo)
            for hypo in G:
                minspecific(hypo,list2,S[0])
            # G has been changed
            for hypo in G:
                if (checkinclude(hypo,list2)):
                    G.remove(hypo)
            G=list(set(G))

     print "after training, G is "+G
     print "after training, S is "+S

train()











