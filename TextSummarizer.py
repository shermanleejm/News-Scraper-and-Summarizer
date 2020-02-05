from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import nltk 
import numpy as np
import pandas as pd 
import re 
import networkx as nx
from gensim.summarization.summarizer import summarize 
from gensim.summarization import keywords 
import string

df = pd.read_csv("text.csv")
df = df.dropna()

articles = {}

stop_words = set(stopwords.words('english'))

def cleanWord(word):
    bad_ch = ",'. :"
    for ch in bad_ch:
        word.replace(ch, " ")
    return word
    # output = ""
    # bad_ch = "()[]{\}/"
    # for ch in word:
    #     if ch in bad_ch:
    #         output += ''
    #     if ch == ",":
    #         output += " "
    #     else :
    #         output += ch
    # return output

for idx, row in df.iterrows():
    if row["headlines"] == "" or row["body"] == "":
        pass
    else :
        body = row['body']
        # articles[row["headlines"]] = row["body"].replace(u"\xa0", " ")
        # articles[row["headlines"]] = re.sub(r'[^\x00-\x7f]',r'', body)
        articles[row['headlines']] = [row["link"], row['body']]

def containsLetters(word) :
    for ch in word:
        if ch in string.ascii_letters:
            return True
    return False

def summarizer(article) :
    article = article.replace(".,", ". ")
    article = article.replace('",', '" ')
    
    sentences = []
    for sent in article.split("."):
        if sent != "":
        # print (sent.strip(","))
            sentences.append(sent.strip())
    
    unique_words = []
    for sent in sentences:
        for word in sent.split(" "):
            if word.lower() not in unique_words and word.lower() not in stop_words:
                unique_words.append(cleanWord(word.lower()))

    sentence_score = {}
    for i in range(len(sentences)):
        sent = sentences[i]
        score = 0
        for word in unique_words:
            if word in sent.lower():
                score += 1
        sentence_score[sent] = score
    arranged = sorted(sentence_score.items(), key=lambda x:x[1], reverse=True)

    top_hits = 5
    
    output = ""
    for sent in arranged[:top_hits]:
        output += sent[0] + " "
    return output
    # print (sort(sentence_score, reverse=True)[:5])

for title, body in articles.items():
    print (title, end="\n\n")
    print (body[0].strip("<200 ").strip(">"), end='\n\n')
    print (summarizer(body[1]), end="\n\n")




# Wuhan coronavirus: Quarantined taxi, private-hire drivers to receive care package