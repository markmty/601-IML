import sys, math

fd1=open(sys.argv[1])
tr_data=fd1.read()
list1=tr_data.split('\n') #list of each line
list1.pop()
fd1.close()


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

    result = float(nk+1)/float(n+vol_num)
    return result

def cal_log_ratio(cat,word):
    temp=math.log(cal_word_prob('lib',word))-math.log(cal_word_prob('con',word))
    if cat=='con':
        temp= -temp
    return temp

lib_ratio_dict={}
for word in lib_dict:
    lib_ratio_dict[word]=cal_log_ratio('lib',word)

con_ratio_dict={}
for word in con_dict:
    con_ratio_dict[word]=cal_log_ratio('con',word)

liblist=[]
for key in lib_ratio_dict:
    temp = (lib_ratio_dict[key],key)
    liblist.append(temp)
liblist.sort(key=lambda tup:tup[0])
liblist.reverse()

conlist=[]
for key in con_ratio_dict:
    temp = (con_ratio_dict[key],key)
    conlist.append(temp)
conlist.sort(key=lambda tup:tup[0])
conlist.reverse()


for i in xrange(20):
    word = liblist[i][1]
    freq = liblist[i][0]
    freq = round(freq,4)
    print word+' '+str(freq)

print ''

for i in xrange(20):
    word = conlist[i][1]
    freq = conlist[i][0]
    freq = round(freq,4)
    print word+' '+str(freq)


