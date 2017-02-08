import sys, math

fd1=open(sys.argv[1])
tr_data=fd1.read()
list1=tr_data.split('\n') #list of each line
list1.pop()
fd1.close()

fd2=open(sys.argv[2])
cmp_data=fd2.read()
list4=cmp_data.split('\n')
list4.pop()
fd2.close()

q=float(sys.argv[3])

lib_filename = []
con_filename = []
for filename in list1:
    if filename[0:3]=="con":
        con_filename.append(filename)
    else:
        lib_filename.append(filename)

# get list of words for files of each category
lib_content = []
con_content = []

for filename in lib_filename:
    fd = open(filename)
    fd_data = fd.read()
    list = fd_data.split('\n')
    list.pop()
    lib_content.extend(list)

for filename in con_filename:
    fd = open(filename)
    fd_data = fd.read()
    list = fd_data.split('\n')
    list.pop()
    con_content.extend(list)

#print lib_content
#print con_content
for i in xrange(len(lib_content)):
    lib_content[i]=lib_content[i].lower()
for i in xrange(len(con_content)):
    con_content[i]=con_content[i].lower()

vol_content = set(lib_content+con_content)
vol_num = len(vol_content)

lib_dict = {}
con_dict = {}

for word in lib_content:
    if word not in lib_dict:
        lib_dict[word] = 1
    else:
        lib_dict[word] +=1

for word in con_content:
    if word not in con_dict:
        con_dict[word] = 1
    else:
        con_dict[word] += 1

#print lib_dict
#print con_dict

def cal_word_prob(cat,word):
    nk=0
    if cat=='lib':
        if word in lib_dict:
            nk = lib_dict[word]
        n =  len(lib_content)
    else :
        if word in con_dict:
            nk = con_dict[word]
        n = len(con_content)

    result = float(nk+q)/float(n+q*vol_num)
    return result

def classify(filename):
    fd = open(filename)
    data = fd.read()
    data = data.split('\n')
    data.pop()
    fd.close()

    for i in xrange(len(data)):
        data[i]=data[i].lower()

    prob_lib= math.log(float(len(lib_filename))/float(len(list1)))
    prob_con= math.log(float(len(con_filename))/float(len(list1)))

    for word in data:
        if word in vol_content:
            prob_lib += math.log(cal_word_prob('lib',word))
            prob_con += math.log(cal_word_prob('con',word))

    if prob_lib>prob_con:
        print "L"
        return "L"
    else:
        print "C"
        return "C"

notes=[]
for file in list4:
    notes.append(classify(file))
#print notes

truth=[]
for filename in list4:
    if filename[0:3]=='lib':
        truth.append('L')
    else:
        truth.append('C')
#print truth

count=0
for i in xrange(len(list4)):
    if notes[i] == truth[i]:
        count += 1

accuracy = float(count)/float(len(list4))
accuracy = round(accuracy,4)
print "Accuracy: "+str(accuracy)



