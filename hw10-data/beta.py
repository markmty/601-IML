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

def beta1():
    pairs = []
    for i in states:
        temp = (i, 0.0)
        pairs.append(temp)
    return dict(pairs)

def beta2(obs,t,beta_mat):
    pairs = []
    for i in states:
        templist=[]
        for j in states:
            temp=beta_mat[t+1][j] + math.log(trans_dict[i][j]) + math.log(emit_dict[j][obs])
            templist.append(temp)
        result = listlogsum(templist)
        pairs.append((i,result))
                       
    return dict(pairs)


def cal_1line(obs):
    T=len(obs)
    i=0
    beta_mat=[]
    while i<T:
        beta_mat.append({})
        i = i+1
    beta_mat[T-1]=beta1()

    for x in xrange(T-1):
        t = T-x-2
        beta_mat[t]=beta2(obs[t+1],t,beta_mat)
    templist=[]
    for i in states:
        temp = math.log(prior_dict[i]) + math.log(emit_dict[i][obs[0]]) + beta_mat[0][i]
        templist.append(temp)
    print listlogsum(templist)


for line in obs_list:
    cal_1line(line)
























