import sys, math, random
import numpy as np

file_name1 = sys.argv[1]

fd1=open(file_name1)
data=fd1.read()
raw_list1=data.split("\n")
fd1.close()

raw_list1.pop(0)
raw_list1.pop(-1)

list1=[[]] * len(raw_list1)
for i in xrange(len(list1)):
    list1[i] = raw_list1[i].split(",")
#print list1

if file_name1=="music_train.csv":
    num_attr = 4
else:
    num_attr = 5

#initialize input from string into numbers
for i in xrange(len(list1)):
    for j in xrange(num_attr+1):
        if (list1[i][j] == "yes") or (list1[i][j] == "yes\r"):
           list1[i][j] = 1.0
        elif (list1[i][j] == "no") :
            list1[i][j] = -1.0
        elif (list1[i][j] == "no\r") :
            list1[i][j] = 0.0
        else:
            if file_name1=="education_train.csv":
                list1[i][j]= float(list1[i][j])/100
            list1[i][j]= float(list1[i][j])
            if list1[i][j]>1899:
                list1[i][j] = (list1[i][j]-1900.0)/100.0

#print list1

truths=[0.0]*len(list1)
for i in xrange(len(list1)):
    truths[i]=list1[i][num_attr]
#print truths


inputs=[[]]*len(list1)
for i in xrange(len(list1)):
    inputs[i]=list1[i][0:(num_attr)]
#print inputs

file_name2= sys.argv[2]

fd2=open(file_name2)
data=fd2.read()
raw_list2=data.split("\n")
fd2.close

raw_list2.pop(0)
raw_list2.pop(-1)

#print raw_list2

list2=[[]] * len(raw_list2)
for i in xrange(len(list2)):
    list2[i] = raw_list2[i].split(",")
#print list2

for i in xrange(len(list2)):
    for j in xrange(num_attr):
        if (list2[i][j] == "yes") or (list2[i][j] == "yes\r"):
            list2[i][j] = 1.0
        elif (list2[i][j] == "no") :
            list2[i][j] = -1.0
        elif (list2[i][j] == "no\r") :
            list2[i][j] = 0.0
        else:
            if file_name2=="education_dev.csv":
                list2[i][j]= float(list2[i][j])/100
            elif list2[i][j]>1899:
                list2[i][j] = (float(list2[i][j])-1900.0)/100.0
            else:
                list2[i][j]= float(list2[i][j])

tests=[[]]*len(list2)
for i in xrange(len(list2)):
    tests[i]=list2[i][0:(num_attr)]
#print tests


def normalize(x):
    if file_name1=="music_train.csv":
        if x>0.5:
            return "yes"
        else:
            return "no"
    else:
        return round(x*100)

def sigmoid(x):
    return 1.0/(1.0+math.exp(-x))

class BP_NN:

    def __init__(self, num_input, num_hiden, num_output):
        self.num_input = num_input+1
        self.num_hiden = num_hiden+1
        self.num_output = num_output

        #initialize
        self.input = np.ones((1, self.num_input))
        self.hiden = np.ones((1, self.num_hiden))
        self.output = np.ones((1, self.num_output))

        #create weights
        self.w_ih = np.zeros((self.num_hiden, self.num_input))
        self.w_ho = np.zeros((self.num_output, self.num_hiden))
        for j in xrange(self.num_hiden):
            for i in xrange(self.num_input):
                self.w_ih[j][i] = random.uniform(-0.8,0.8)
    #print self.w_ih
        for k in xrange(self.num_output):
            for j in xrange(self.num_hiden):
                self.w_ho[k][j] = random.uniform(-0.8,0.8)
#print self.w_ho

    def calculate(self, input):
        for i in xrange(self.num_input-1):
            self.input[0][i] = input[i]

        for j in xrange(self.num_hiden-1):
            temp=np.dot(self.w_ih, np.transpose(self.input))
            self.hiden[0][j]=sigmoid(temp[j][0])
        #print self.hiden

        for k in xrange(self.num_output):
            temp=np.dot(self.w_ho, np.transpose(self.hiden))
            self.output[0][k] = sigmoid(temp[k][0])
    #print self.output
    
        return self.output[0][0]

    def backpropagation(self, truth, learn_rate):
        #calculate error of outputs
        err_output = [0.0]* self.num_output
        for k in xrange(self.num_output):
            err = truth[k] - self.output[0][0]
            err_output[k] = err*(self.output[0][k])*(1-(self.output[0][k]))

        #calculate error of hidden layer
        err_hiden = [0.0] * self.num_hiden
        for j in xrange(self.num_hiden):
            err = 0.0
            for k in xrange(self.num_output):
                err += err_output[k]*self.w_ho[k][j]
            err_hiden[j]=err*(self.hiden[0][j])*(1-(self.hiden[0][j]))
        

        # update weights
        for j in xrange(self.num_hiden):
            for k in xrange(self.num_output):
                self.w_ho[k][j] += learn_rate*err_output[k]*self.hiden[0][j]

        for i in xrange(self.num_input):
            for j in xrange(self.num_hiden):
                self.w_ih[j][i] += learn_rate*err_hiden[j]*self.input[0][i]

        #print self.w_ih

                    

    def cal_error(self, trainings, truths ):
        predictions = [0.0] * len(truths)
        for i in xrange(len(predictions)):
            predictions[i] = self.calculate(trainings[i])
        
        error = 0.0
        for k in xrange(len(truths)):
            error += 0.5*(predictions[k]-truths[k])**2

        return error

    def train(self, inputs, truths):
        for i in xrange(len(inputs)):
            self.calculate(inputs[i])
            self.backpropagation([truths[i]], 0.2)
                #print self.w_ih
        print self.cal_error(inputs,truths)

    def predict(self, inputs):
        for i in xrange(len(inputs)):
            temp= self.calculate(inputs[i])
            print normalize(temp)



n=BP_NN(num_attr,num_attr,1)

#n.calculate(inputs[0])
#n.backpropagation([truths[0]],0.1)
#n.calculate(inputs[1])
#n.backpropagation([truths[1]],0.1)

for i in xrange(1000):
    n.train(inputs,truths)
print "TRAINING COMPLETED! NOW PREDICTING."
n.predict(tests)














