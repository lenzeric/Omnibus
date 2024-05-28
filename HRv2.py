#Python program to determine user-defined appropriations in omnibus bill HR2617.
#Author: Eric Lenz, PhD

#Update (5/27/24): I made the program more user-friendly with match amounts, search numbers, and an exit path. Also, the program generates a bar plot that updates with each keyword search.

#Description
#This program loops through a large omnibus bill to determine appropriations related to user-defined keywords like 'covid-19' or 'infrastructure'. Then, it creates a dataframe of the dollar amounts and sums them. 

#Ultimately, I want to create an index of appropriations for analysis and potential investment. Future updates will allow for a download of the data set.

#The HR2617 bill (102,158 lines of text): https://www.congress.gov/bill/117th-congress/house-bill/2617

#Directions
#Save the text file "HR2617.txt" in your working directory. I had issues using urllib.request...getting HTTP Error 403: Forbidden. Also, the link to XML/HTML is super slow. Therefore, just copy/paste the bill into a text file, save into your working directory, and read in with BeautifulSoup.

#Code also borrowed from:
#https://stackoverflow.com/questions/51691270/python-user-input-as-regular-expression-how-to-do-it-correctly
#https://medium.com/codex/a-beginners-guide-to-easily-create-a-word-cloud-in-python-7c3078c705b7
#https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
#https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
#https://www.studysmarter.co.uk/explanations/computer-science/computer-programming/python-infinite-loop/
#https://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists
#https://www.geeksforgeeks.org/pandas-concat-function-in-python/
#https://stackoverflow.com/questions/21487329/add-x-and-y-labels-to-a-pandas-plot

#In the command line, be sure to install the following packages.
#pip install requests
#pip install bs4
#pip install wordcloud
#pip install pillow
#pip install nltk
#python -m nltk.downloader all
#pip install pandas

from wordcloud import WordCloud
from PIL import Image
import requests
from bs4 import BeautifulSoup, UnicodeDammit
import urllib.request
import re
import pandas as pd
import matplotlib.pyplot as plt
#import numpy

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

hand = open('HR2617.txt')
soup = BeautifulSoup(hand, 'html.parser')
text = soup.get_text(" ", strip=True)
sent = sent_tokenize(text)
#print(sent)

#Make the sentences lower case and remove stop words.
low_words = [w.lower() for w in sent]
remove_words = [w for w in low_words if w not in stopwords.words('english')]
#print(remove_words)

#There are 15 departments in the US federal government. These are likely keyword matches in the bill.
#depts = ['department of health and human services', 'department of defense', 'department of labor', 'department of agriculture', 'department of veterans affairs', 'department of interior', 'department of transportation', 'department of justice', 'department of education', 'department of housing and urban development', 'department of homeland security', 'department of energy', 'department of treasury', 'department of state', 'department of commerce']

#Other interesting key words.
#other = ['assistance', 'security', 'ukraine', 'military', 'education', 'act', 'grant', 'transportation', 'personnel', 'infrastructure', 'energy', 'indigenous', 'nongovernmental']

counter = 0

while True:
    counter += 1
    
    print("\nPlease type 'exit' if you wish to exit the program.")
    user_input = input("Keyword search (lowercase):")
    if user_input == "exit":
        break
    
    mlist = list()
    count = 0
    for line in remove_words :
        line = line.rstrip()
        x = re.compile(user_input).findall(line)
        y = re.findall(r'\$[0-9,]+', line)
        if len(x) <1 : continue
        mlist.append(y)
        count = count + 1

    if mlist != list([]):
        list_words = sum(mlist,[])
        dlist = list()
        for dollar in range(len(list_words)):
            punc_words = list_words[dollar].replace('$', '').replace(',', '')
            pnums = int(punc_words)
            dlist.append(pnums)

        df = pd.DataFrame(dlist)
        df2 = df.drop_duplicates()
        df2=df2.rename({})
        df2.rename(columns={ df2.columns[0]: str(user_input) }, inplace = True)
        
        if 'df3' in locals():
            df3 = pd.concat([df2, df3], axis=1)
        else:
            df3 = df2
        print("There are", len(df2[str(user_input)]), "matches for", str(user_input), "without duplicate appropriations.")

        print('Sum of appropriations for', str(user_input), 'search #', str(counter), 'in USD: ', "$", df2[str(user_input)].sum())

        Total = df3.sum(axis=0)
        Tplot = Total.plot.bar(rot=0, title='Appropriation Search Results')
        Tplot.set_xlabel("Keywords")
        Tplot.set_ylabel("Appropriations (USD)")
        plt.show()
    
    else:
        print("Sorry, there are no matches.")
        break
