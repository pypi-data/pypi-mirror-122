# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 15:28:59 2021

@author: Sumayyah Taiwo
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr


class EDA:
    """ class for Exploratory Data Analysis for csv file"""
    def __init__(self, file_path): 
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        self.info = self.df.info()
        #self.describe = self.df.describe()
        #Splits data into train and test
        #self.train, self.test = train_test_split(self.df, train options)
        
    def cat_var(self):
       """ returns a tuple of the number and the list of categorical variables """
       cat_bool = (self.df.dtypes == 'object') 
       categorical = list(cat_bool[cat_bool].index)
       return len(categorical), categorical
       
    def num_var(self):
        """ returns a tuple of the number and the list of numerical variables """
        num_bool = (self.df.dtypes != 'object') 
        numerical = list(num_bool[num_bool].index)
        return len(numerical), numerical
   
    def null_cat(self):
        """ returns a tuple of the number and the list of categorical variables containing null values """
        null_bool = (self.df.isnull().sum() != 0)
        null = list(null_bool[null_bool].index)
        null_categorical = [i for i in self.cat_var()[1] if i in null]
        return len(null_categorical), null_categorical
   
    def null_num(self):
        """ returns a tuple of the number and the list of numerical variables containing null values """
        null_bool = (self.df.isnull().sum() != 0)
        null = list(null_bool[null_bool].index)
        null_categorical = [i for i in self.num_var()[1] if i in null]
        return len(null_categorical), null_categorical
    
    def cat_viz(self, target):
        """returns a countplot of each categorical variable using target as hue"""
        self.target = target
        for i in self.cat_var()[1]:
            sns.catplot(data= self.df,x=i,kind='count',hue = self.target)
            plt.show()
            plt.title(i)
       
    def num_viz(self, target):
        """returns histogram and boxplot for each categorical variable using target as hue"""
        self.target = target
        for i in self.num_var()[1]:
            plt.hist(self.df[i])
            plt.title(i)
            plt.show()
            plt.legend(self.df[target])
            
        for i in self.num_var()[1]:
            sns.boxplot(self.df[i])
            plt.title(i)
            plt.show()
            plt.legend(self.df[target])
        
    def outliers(self):
        """returns a tuple containing the list of numerical features containing outliers,
        the number of outliers therein, the first, second, third and fourth quartile,
        the lower and upper threshold as well as the Interquartile range
        """
        
        result = []
        for i in self.df[self.num_var()[1]]:
            count=0
            IQR = iqr(self.df[i])
            Q = np.quantile(self.df[i],[0,0.25,0.5,0.75,1])
            lower_threshold = np.quantile(self.df[i],0.25)-1.5*IQR
            upper_threshold = np.quantile(self.df[i],0.75)+1.5*IQR
            for k in self.df[i]:
                if k<lower_threshold or k>upper_threshold:
                    count += 1
                else:
                    count += 0
            result.append(print(i,':outliers =',count,',lower_threshold =',lower_threshold ,',upper_threshold =',upper_threshold,
                                'Q1 =',Q[1],',Q2 =',Q[2],',Q3 =',Q[3],',Q4 =',Q[4],',iqr =',IQR))
            return result

