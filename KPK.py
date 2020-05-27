import math as m
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
data = np.genfromtxt('kpk.txt', skip_header=7, delimiter='')

# sort
n=0
for i in data[:, 2]:
    if i > 0 or i==0: n+=1
    if i < 0: break
t=data[n:, 0]
E=[i/1000 for i in data[n:, 1]]
i=[i/1000000 for i in data[n:, 2]]
###
plt.figure(figsize=(7.5, 6))
ax1=plt.subplot(211)
ax1.plot(E,i)
plt.xlabel('E, B')
plt.ylabel('i, A')
######
ax2=plt.subplot(212)
lgi=[]
for j in i:
    lgi.append(np.log10(-1*j))
ax2.plot(lgi, E)
plt.xlabel('lg(i)')
plt.ylabel('E, B')
plt.show()
###
plt.figure(figsize=(7.5, 6))
pt=int(input('potential'))
ax1=plt.subplot(221)
ax1.plot(E,i)
plt.xlabel('E, B')
plt.ylabel('i, A')
ax2=plt.subplot(223)
ax2.plot(lgi, E)
plt.xlabel('lg(i)')
plt.ylabel('E, B')
n=0
for i in data[:, 1]:
    if i > pt:
        n+=1
    if i < pt:
        break
i1=[i/1000000 for i in data[n:, 2]]
lgi1=[]
for j in i1:
    lgi1.append(np.log10(-1*j))
E1=[-1*i/1000 for i in data[n:, 1]]
z_1= np.polyfit(lgi1,E1, 1)
y_2 = np.poly1d(z_1)(lgi1)
ax3=plt.subplot(122)
ax3.plot(lgi1,E1)
plt.xlabel('lg(i)')
plt.ylabel('-E, B')
ax3.plot(lgi1, y_2, "r--", lw=1)
text = f"$y={z_1[0]:0.4f}\;x{z_1[1]:+0.4f}$\n$R^2 = {r2_score(E1, y_2):0.3f}$"
plt.gca().text(0.05, 0.8, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
plt.show()
a=z_1[1]
b=z_1[0]
itr=10**(-1*a/b)
Kper=2.3*8.314*298/(96495*b)
print('a=',a,'\n','b=',b,'\n','i(обмена)',itr,'\n','коэф.переноса',Kper)