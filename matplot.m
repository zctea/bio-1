figure(1)
clf   
m=csvread("GSE33147.pcc")
surf(m)
print -dpng GSE33147_T50.png
