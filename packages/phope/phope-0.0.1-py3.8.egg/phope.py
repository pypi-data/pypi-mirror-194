import pandas as pd
import numpy as np
from sklearn.metrics import r2_score as r2
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from pathlib import Path
p=Path('./data.csv')
if p.is_file():
 d=pd.read_csv('data.csv')
else:
 print('create a data.csv file')
 exit()
degree1=int(d.degree1[0])
degree2=int(d.degree2[0])
from datetime import date
first=date(int(d.day[0].split('/')[0]),int(d.day[0].split('/')[1]),int(d.day[0].split('/')[2]))
days=len(d.day)-1
target=date(int(d.day[days].split('/')[0]),int(d.day[days].split('/')[1]),int(d.day[days].split('/')[2]))
X=[]
X.append(0)
for i in range(1,days+1):
 dd=date(int(d.day[i].split('/')[0]),int(d.day[i].split('/')[1]),int(d.day[i].split('/')[2]))
 X.append((dd-first).days)
def main():
 fig,ax1=plt.subplots()
 ax2 = ax1.twinx()
 ax1.set_xticklabels(d.day,rotation=90)  
 ax1.set_xticks(X)
 model_hb=np.poly1d(np.polyfit(X[0:days],d.hgb[0:days],degree1))
 hgb_error=r2(model_hb(X[0:days]),d.hgb[0:days])
 x1=(target-first).days
 y1=model_hb(x1)
 print(model_hb.coefficients)
 print('hbA1c: ',round(y1,3))
 d.hgb[days]=y1
 plt.ylim(5,9)
 ax1.plot(X[0:days],d.hgb[0:days],marker='x')
 ax1.plot(X[days],d.hgb[days],color='r',marker='x')
 ax1.legend(['hbA1c'],loc=3,bbox_to_anchor= (0.7, 0.7))
 plt.ylim(0,450)
 ax2.set_xticklabels(d.day,rotation=90)  
 ax2.set_xticks(X)
 model_bnp=np.poly1d(np.polyfit(X[0:days],d.ntbnp[0:days],degree2))
 ntbnp_error=r2(model_bnp(X[0:days]),d.ntbnp[0:days])
 x1=(target-first).days
 y1=model_bnp(x1)
 print(model_bnp.coefficients)
 print('NT-proBNP: ',round(y1,3))
 d.ntbnp[days]=y1
 ax2.plot(X[0:days],d.ntbnp[0:days],marker='o')
 ax2.plot(X[days],d.ntbnp[days],color='r',marker='o')
 ax2.legend(['NT-proBNP'],loc=3,bbox_to_anchor= (0.7, 0.6))
 plt.text(20,90,'r2_hgb: '+str(round(hgb_error,3)))
 plt.text(70,90,'degree: '+str(degree1))
 plt.text(20,60,'r2_ntbnp: '+str(round(ntbnp_error,3)))
 plt.text(70,60,'degree: '+str(degree2))
 plt.savefig('hba1c_ntbnp.png',bbox_inches='tight')
 plt.show()
main()
