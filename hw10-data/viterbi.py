import sys,math

observation_name = sys.argv[1]
trans_name = sys.argv[2]
emit_name = sys.argv[3]
prior_name = sys.argv[4]


#===================================================
#obs_list, trans_dict, emit_dict, prior_dict
#===================================================

# pre-do with dev.txt
fd1=open(observation_name)
dev_data = fd1.read()
dev_list = dev_data.split("\n")
dev_list.pop()
fd1.close()

def observation_init(dev_list):
    temp = []
    for sentence in dev_list:
        stc_list = sentence.split(" ")
        temp.append(stc_list)
    return temp

obs_list = observation_init(dev_list)

#pre-do with trans
fd2=open(trans_name)
trs_data = fd2.read()
trs_list = trs_data.split("\n")
trs_list.pop()
fd2.close()

def line2dict(line):
    list = line.split(" ")
    tag = list[0]
    list.pop(0)
    list.pop()
    pairs=[]
    for element in list:
        elm=element.split(":")
        pairs.append((elm[0],float(elm[1])))
    d = dict(pairs)
    return (tag,d)

def file_init(trs_list):
    temp = []
    for stc in trs_list:
        tuple = line2dict(stc)
        temp.append(tuple)
    return dict(temp)

trans_dict = file_init(trs_list)

#pre-do with emit
fd3 = open(emit_name)
emit_data = fd3.read()
emit_list = emit_data.split("\n")
emit_list.pop()
fd3.close()
emit_dict = file_init(emit_list)

#pre-do with prior
fd4 = open(prior_name)
prior_data = fd4.read()
prior_list = prior_data.split("\n")
prior_list.pop()
fd4.close()

def prior_init(prior_list):
    temp=[]
    for line in prior_list:
        l = line.split(" ")
        temp.append((l[0],float(l[1])))
    return dict(temp)

prior_dict = prior_init(prior_list)

states = prior_dict.keys()
#print states
#===================================================
# calculate helper
#===================================================
def log_mlt(x1,x2):
    temp = math.log(x1) + math.log(x2)
    return temp

def log_sum(left,right):
    if right < left:
        return left + math.log1p(math.exp(right - left))
    elif left < right:
        return right + math.log1p(math.exp(left - right))
    else:
        return left + math.log1p(1)

def listlogsum(list):
    head=list[0]
    list.pop(0)
    for element in list:
        head = log_sum(head,element)
    return head

#===================================================
#
#===================================================

def VP1(obs):
    pairs = []
    for i in states:
        temp = math.log(prior_dict[i])+math.log(emit_dict[i][obs])
        tuple = (i, (i,temp))
        pairs.append(tuple)
    return dict(pairs)

def Q1():
    pairs = []
    for i in states:
        pairs.append((i,[i]))
    return dict(pairs)

def VP2(obs,t,VP_mat):
    pairs = []
    for i in states:
        templist=[]
        for j in states:
            temp=VP_mat[t][j][1]+math.log(trans_dict[j][i])+math.log(emit_dict[i][obs])
            templist.append((j,temp))
        templist.sort(key=lambda tup:tup[1])
        templist.reverse()
        result = templist[0]
        pairs.append((i,result))
                       
    return dict(pairs)

def Q2(t,obs,Q_mat,VP_mat):
    pairs=[]
    for i in states:
        k=VP_mat[t+1][i][0]
        temp=Q_mat[t][k]
        result=temp+[i]
        pairs.append((i,result))
    
    return dict(pairs)

def findmax(dict):
    temp=[]
    for key in dict:
        tuple=(key,dict[key][1])
        temp.append(tuple)
    temp.sort(key=lambda tup:tup[1])
    temp.reverse()
    return temp[0][0]

def cal_1line(obs):
    T=len(obs)
    i=0
    VP_mat=[]
    Q_mat=[]
    while i<T:
        VP_mat.append({})
        Q_mat.append({})
        i = i+1
    VP_mat[0]=VP1(obs[0])
    Q_mat[0]=Q1()
    for t in xrange(T-1):
        VP_mat[t+1]=VP2(obs[t+1],t,VP_mat)
#print VP_mat

    for t in xrange(T-1):
        Q_mat[t+1]=Q2(t,obs[t+1],Q_mat,VP_mat)
#print Q_mat[T-1]
    key = findmax(VP_mat[T-1])
    ans = Q_mat[T-1][key]
    temp=[]
    string=''
    for i in xrange(T):
        string += obs[i]+'_'+ans[i]+' '
    print string[0:-1]


for line in obs_list:
    cal_1line(line)
























