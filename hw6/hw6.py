import sys, math

file_Name = sys.argv[1]

fd=open(file_Name)
data=fd.read()
raw_list=data.split("\n")
fd.close()

x_list=[]
y_list=[]
xy_list=[]

for pair in raw_list:
    pair_list=pair.split()
    x_list.append(float(pair_list[0]))
    y_list.append(float(pair_list[1]))
    xy_list.append(float(pair_list[0])*float(pair_list[1]))


def square(x): return x*x

#expectation
x_expectation= float(sum(x_list))/len(x_list)
y_expectation= float(sum(y_list))/len(y_list)
xy_expectation=float(sum(xy_list))/len(xy_list)
xx_expectation=float(sum(map(square,x_list)))/len(x_list)
print "x_expectation = "+str(x_expectation)
print "y_expectation = "+str(y_expectation)

def pvariance(list):
    exp=sum(list)/len(list)
    total=0
    for element in list:
        total+=square(element-exp)
    return total/len(list)

#variance
x_var= pvariance(x_list)
y_var= pvariance(y_list)
print "x_var = "+str(x_var)
print "y_var = "+str(y_var)

#linear regression
beta=(xy_expectation-x_expectation*y_expectation)/(xx_expectation-x_expectation*x_expectation)
alpha=y_expectation-beta*x_expectation
print "beta = "+str(beta)
print "alpha = "+str(alpha)

#correlation
cov=xy_expectation-x_expectation*y_expectation
corr=cov/(math.sqrt(x_var)*math.sqrt(y_var))
print "corr = "+str(corr)
