# -*- coding: utf-8 -*-
"""
Spyder Editor
@author: Rushabh Sancheti
This is a temporary script file.
"""
import pandas as pd
class CS: 
    df=list()
    no=0
    n=0
    y=0
    yes=0  
    def Csvreader(self,filename):
        data=pd.read_csv(open(filename,"rt"))
        return(data)
    
    def dataCleaning(self,data):
        print(len(data))
        val3=data['3. Diastolic blood pressure (mm Hg)'].mean()
        val4=data['4. Triceps skin fold thickness (mm)'].mean()
        val5=data['5. 2-Hour serum insulin (mu U/ml)'].mean()
        val6=data[' 6.Body mass index '].mean()
        
        for i in range(len(data)): 
            if(data['3. Diastolic blood pressure (mm Hg)'][i]==0):
                data['3. Diastolic blood pressure (mm Hg)'][i]=val3
            if(data['4. Triceps skin fold thickness (mm)'][i]==0):
                data['4. Triceps skin fold thickness (mm)'][i]=val4    
            if(data['5. 2-Hour serum insulin (mu U/ml)'][i]==0):
                data['5. 2-Hour serum insulin (mu U/ml)'][i]=val5
            if(data[' 6.Body mass index '][i]==0):
                data[' 6.Body mass index '][i]=val6
        return data        
              
    def BinningNew(self,data):
        for i in range(8):
            data.iloc[:,i] = pd.cut(data.iloc[:,i],bins=3, labels=['Bad', 'Average', 'Good'],include_lowest=True)
        data.iloc[:,8] = pd.cut(data.iloc[:,8],bins=2, labels=['No', 'Yes'],include_lowest=True)    
            
        return data    
    
    def naiveBayes(self,data):
        temp=data.groupby([' 9. Class variable (0 or 1)']).size()
        ob.n=temp[0]
        ob.y=temp[1]
        ob.yes=temp[1]/len(data)
        ob.no=temp[0]/len(data)
        for i in range(8):
            ob.df.append(data.groupby([data.iloc[:,i],data.iloc[:,8]]).size())  
      #  print(ob.df)    
        return data
    
    def naiveBayesValidation(self , test):
        lst=list()
        for i in range(len(test)):
            valy=1.0
            valn=1.0
            
            for j in range(8):
                if(test.iloc[i][j]=='Bad'):
                    valn=valn*int(ob.df[j][0])/ob.n   
                    valy=valy*ob.df[j][1]/ob.y
                elif(test.iloc[i][j]=='Average'):
                    valn=valn*ob.df[j][2]/ob.n
                    valy=valy*ob.df[j][3]/ob.y
                else:
                    valn=valn*ob.df[j][4]/ob.n
                    valy=valy*ob.df[j][5]/ob.y
            valn=valn*ob.no
            valy=valy*ob.yes
            if((valn)>(valy)):
                lst.append('No')
            else:
                lst.append('Yes')
                
        count=0
        for i in range(len(test)):
            if(test.iloc[i][8]==lst[i]):
                count=count+1 
        print(count)        
        print("accuracy percenatage={:03.2f}%".format(count/len(test)*100))   
        fn=0
        tp=0
        fp=0
        tn=0
        for i in range(len(test)):
            if(test.iloc[i][8]=='Yes' and lst[i]=='Yes'):
                tp=tp+1
            elif(test.iloc[i][8]=='Yes' and lst[i]=='No'):
                tn=tn+1  
            elif(test.iloc[i][8]=='No' and lst[i]=='Yes'):
                fp=fp+1
            else:
                fn=fn+1    
        
        print("confusion matrix")
        print("                      actual yes       actual no" )
        print("Predicted yes         ",tp,"                ",fp)
        print("Predicted no          ",tn,"                ",fn)
        

ob=CS()
data=ob.Csvreader("pima-indians-diabetes.csv")     #load data from csvfile into dataframe
data=ob.dataCleaning(data)                          #clean the data for missing value  
data=ob.BinningNew(data)                            #covert numerical data into categorical data
train = data.iloc[0:600]                            #Loading data into test data
test = data.iloc[601:768]                           #Loading data into training data
ob.naiveBayes(train)                                #preparing predictive model  
ob.naiveBayesValidation(test)                       #checking for correctness aof algorithm
