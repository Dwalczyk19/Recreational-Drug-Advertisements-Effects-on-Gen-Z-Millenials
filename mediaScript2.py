# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 00:54:55 2022

@author: Dave
"""

'''MEDIA & SOCIETY SCRIPT PART2

Focusing on the effect of recreational drug advertisements over an average age interval of 17-30
Will use pandas for easier analysis and visualization; matplotlib's pyplot for direct visuals; and 
potentially numpy. 

Use of R & ggplot2 could be useful in visualization and certain statistical methods, however the data
in this instance is not directly numerical & quantitative but more qualitative and is a total measure, 
not a regression technique capable with strictly numerical data 

Nevertheless, a few inferences will be made as a result of data analysis; the plan is for this list 
to be expanded and more infeneces to be created, however given limited data & more qualitative data, 
machine learning or forms of NLP might be needed in order to expand research.

- Average age 
- Male to Female Ratio, the amount of Yes (Y) & No (N) responses per gender #Pandas .corr could come in handy
- If under 21 what is the ratio of Y or N to q1 
- Ratio on q2, check its effect with optional q4
- Average % of Y & Y, N & N, Y & N, Y & Y & Y. Divide the amounts of these values by 3+, 5 'Response' 
Intervals. This is very similar to large datasets where the total % is within the much higher 'Response' 
counts
- Based on the data is it true that people under 21 are more likely to go out and purchase/consume 
recreational drugs? 
'''


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import csv 


def piePlot(names,vals):
    names = np.array(names)
    lowest = vals.index(min(vals))
    explode = [0,0,0,0]
    explode[lowest] += 0.1
    explode = tuple(explode)
    
    fig, axis = plt.subplots()
    axis.pie(vals, explode=explode, labels=names, autopct="%1.1f%%",
             shadow=True, startangle=90)
    axis.axis('equal')
    
    plt.show()
    
def labels(x,y, avg): 
    for i in range(len(x)): 
        plt.text(i,y[i],avg[i], ha="center")
            
    
def plot(uni):                   
    #Plot a histogram measuring the total amount of q5's responses with is respective key
    #on top of each bar will be the the average age of that response 
    
    x = list(uni.keys())
    y = [len(items) for items in uni.values()]
    avg = [round(sum(items) / len(items), 3) if len(items) > 0 else 0 for items in uni.values()]
    
    plt.figure(figsize = (10,5))
    plt.bar(x,y)
    
    labels(x,y,avg)
    
    plt.xlabel("Type of Question Responses")
    plt.ylabel("Amount")
    
    plt.title("Average age of Responses")
    
    plt.show()

    
def VisualEase(data,idx): 
    return data.loc[idx]


if __name__ == "__main__":
    data = pd.read_csv("ProjectData.csv")
    
    #1
    for headers in data.columns: 
        data.rename(columns = {"age ": "age"}, inplace=True)
        if ( headers.startswith("q") ):
            data.pop(headers)
            
            
    averageAge = data["age"].mean().round(2)
    medianAge = data["age"].median()
    modeAge = data["age"].mode()
    
    
    #2
    M = 0
    F = 0
    nullAmount = 0
    genderFreq = {"M":M, "F":F, "N/A":nullAmount}
    
    for items in data.columns:
        if items == "gender":
            for values in data[items]:
                if values == "M":
                    genderFreq["M"] += 1
                elif values == "F": 
                    genderFreq["F"] += 1
                else: 
                    genderFreq["N/A"] += 1

    
    
    #3
    '''
    Divide the dictionary into 4 sections: 
    (1) 21+ and Yes 
    (2) <21 and Yes 
    (3) 21+ and No 
    (4) <21 and No
    '''
    ageToQ1 = {"1":0, "2":0, "3":0, "4":0}
    ageRows = data["age"] 
    a1 = data["a1"]
    a2 = data["a2"]
    a3 = data["a3"]
    a4 = data["a4"]
    
    ageL = np.sort(ageRows, order=None)
    
    for i in range(len(ageRows)):
        if ageRows[i] >= 21: 
            if a1[i] == "Y": 
                ageToQ1["1"] += 1
            elif a1[i] == "N": 
                ageToQ1["3"] += 1
        else: 
            if a1[i] == "Y": 
                ageToQ1["2"] += 1
            elif a1[i] == "N": 
                ageToQ1["4"] += 1
          
    q3Names = ["21+ & Y", "<21 & Y", "21+ & N", "<21 & N"]
    q3Vals = list(ageToQ1.values())
    #piePlot(q3Names, q3Vals)

    
    #4
    totalIncomeClass = len(data)
    checkZero = 0
    total = a4.sum()
    
    for i in range(len(a4)): 
        if a4[i] == 0: 
            checkZero += 1
     
        
    
    #this is seperate from the main theme of research as we are looking to assess the 
    #age interval specified and whether or not the questions show a pattern of commonality, 
    #instead of by income class (also ask yourself whether the ages in comparison to their income class
    #show a pattern)
    
    #income & yes or no response (idx 0 is YES, while idx 1 is NO)
    upperVals = [0,0]  #upper middle and wealthy (3 & 4)
    middleVals = [0,0] #strictly middle (2)
    lowerVals = [0,0] #lower (1)
    
    
    for i in range(len(a2)): 
        if a4[i] >= 3:  #upper middle class and wealthy
            if a2[i] == "Y":
                upperVals[0] += 1
            elif a2[i] == "N":
                upperVals[1] += 1
        elif a4[i] == 2: #middle class
            if a2[i] == "Y": 
                middleVals[0] += 1
            elif a2[i] == "N": 
                middleVals[1] += 1
                
    
            
    
    #5 
    length = len(data)
    '''#uncomment for visual ease of dataframe
    for i in range(length):
        visualDF = VisualEase(data, i) 
        print(visualDF)
    '''   
    universal = { "YY":[], "YN":[], "NN":[], "NY":[], "YYY":[], "NNN":[], "YNY":[], "NYN":[] }

    for i in range(length): 
        if a1[i] == "Y":
            if a2[i] == "Y":
                universal["YY"].append(ageRows[i])
                if a3[i] == "Y": 
                    universal["YYY"].append(ageRows[i])
                
            elif a2[i] == "N":
                universal["YN"].append(ageRows[i])
                if a3[i] == "Y":
                    universal["YNY"].append(ageRows[i])
        elif a1[i] == "N":
            if a2[i] == "N":
                universal["NN"].append(ageRows[i])
                if a3[i] == "N":
                    universal["NNN"].append(ageRows[i])
            
            elif a2[i] == "Y": 
                universal["NY"].append(ageRows[i])
                if a3[i] == "N":
                    universal["NYN"].append(ageRows[i])
                    
    
    plot(universal)
    
