#Python program to determine user-defined appropriations in omnibus bill HR2617.
#Author: Eric Lenz, PhD

#Description
#This program loops through a large omnibus bill to determine appropriations related to user-defined keywords like 'covid-19' or 'infrastructure'. Then, it creates a dataframe of the dollar amounts and sums them. Ultimately, I want to create an index of appropriations related to private industries, government organizations, housing, and labor for analysis and potential investment.

#The HR2617 bill (102,158 lines of text): https://www.congress.gov/bill/117th-congress/house-bill/2617

#Directions
#Save the text file "HR2617.txt" in your working directory. I had issues using urllib.request...getting HTTP Error 403: Forbidden. Also, the link to XML/HTML is super slow. Therefore, just copy/paste the bill into a text file, save into your working directory, and read in with BeautifulSoup.

#Code also borrowed from:
#https://stackoverflow.com/questions/51691270/python-user-input-as-regular-expression-how-to-do-it-correctly
#https://medium.com/codex/a-beginners-guide-to-easily-create-a-word-cloud-in-python-7c3078c705b7

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
depts = ['department of health and human services', 'department of defense', 'department of labor', 'department of agriculture', 'department of veterans affairs', 'department of interior', 'department of transportation', 'department of justice', 'department of education', 'department of housing and urban development', 'department of homeland security', 'department of energy', 'department of treasury', 'department of state', 'department of commerce']

#Other interesting key words.
other = ['assistance', 'security', 'ukraine', 'military', 'education', 'act', 'grant', 'transportation', 'personnel', 'infrastructure', 'energy', 'indigenous', 'nongovernmental']

#I set up the loop with a user input: simply type in your keyword in lowercase to receive a sum of related appropriations.
user_input = input("Keyword search (lowercase):")  # check console, it is expecting your input

#Loop through sentences (remove_words). The variable x denotes a match with a user-defined keyword like 'covid-19'. Then for each x where x is not less than 1 (non-empty such that one or more matches are found in each line), append a list of dollar amounts associated with those matches (i.e. dollar amounts found in the same sentence). 
mlist = list()
count = 0
for line in remove_words :
    line = line.rstrip()
    x = re.compile(user_input).findall(line)
    y = re.findall(r'\$[0-9,]+', line)
    if len(x) <1 : continue
    mlist.append(y)
    count = count + 1

#Create a list without empty spaces. Some sentences have matches with the keyword, but not dollar amounts. I'm just concerned with dollar amounts associated with the keywords.
list_words = sum(mlist,[])
#print(list_words)

#Remove punctuation like dollar signs and commas. Then, convert the strings in the list to numbers. Result should be whole numbers in dollars (no decimals).
dlist = list()
for dollar in range(len(list_words)):
    punc_words = list_words[dollar].replace('$', '').replace(',', '')
    pnums = int(punc_words)
    dlist.append(pnums)
#print(dlist)

#Create a data frame with Pandas and drop duplicates.
df = pd.DataFrame(dlist)
df2 = df.drop_duplicates()
#print(df2)

#Sum the appropriations.
Total = df2[0].sum()
print('Sum of appropriations in USD: ', Total)