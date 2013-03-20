data=csvread("GPL199.mat")
tdata = data.'
pdata=cor(tdata)
csvwrite("GPL199.pcc",pdata)
