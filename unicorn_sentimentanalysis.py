w# -*- coding: utf-8 -*-
"""Unicorn_SentimentAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ebsAQGLarTCWOyD91C3glEsG6S21Xh4e

# **1. Import and Read the Dataset**
---
The corpus/dataset is imported and displayed.
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import matplotlib.pyplot as plt
import re
# nltk
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
#build the classifier model - logistic regression with tfidf
from sklearn.linear_model import LogisticRegression

#Read the Dataset in pandas and obtain number of data and its columns
cols  = ["sentiment", "ids", "date", "flag", "user", "text"]
enc = "ISO-8859-1"
df=pd.read_csv('sentiment.csv', encoding = enc, names = cols)
print(df.shape)
df.head()

# Removing the unnecessary columns.
df = df[['sentiment','text']]
# Replacing the values to ease understanding.
df['sentiment'] = df['sentiment'].replace(4,1)

# Plotting the distribution for df.
ax = df.groupby('sentiment').count().plot(kind='bar', title='Distribution of data',
                                               legend=False)
ax.set_xticklabels(['Negative','Positive'], rotation=0)

# Storing data in lists.
text, sentiment = list(df['text']), list(df['sentiment'])

"""# **2. Text Preprocessing**


---
Text preprocessing simply means to bring the text into a form that is predictable and analyzable for this task.
Unwanted words or characters that will not contribute to the classification and clustering will be removed.
Example of unwanted words or characters are:-

- Stop Words (is, the, are)
- Digits (0,9)
- Punctuations (./?!)



"""

## Defining set containing all stopwords in english.
stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
             'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
             'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
             'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',
             'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
             'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
             'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
             'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
             'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're',
             's', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
             't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
             'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
             'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
             'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
             'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
             "youve", 'your', 'yours', 'yourself', 'yourselves']

def preprocess(textdata):
    processedText = []

    # Create Lemmatizer and Stemmer.
    wordLemm = WordNetLemmatizer()

    # Defining regex patterns.
    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    sequencePattern   = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"

    for tweet in textdata:
        tweet = tweet.lower()

        # Replace all URls with 'URL'
        tweet = re.sub(urlPattern,' URL',tweet)
        # Replace @USERNAME to 'USER'.
        tweet = re.sub(userPattern,' USER', tweet)
        # Replace all non alphabets.
        tweet = re.sub(alphaPattern, " ", tweet)
        # Replace 3 or more consecutive letters by 2 letter.
        tweet = re.sub(sequencePattern, seqReplacePattern, tweet)

        tweetwords = ''
        for word in tweet.split():
            # Checking if the word is a stopword.
            #if word not in stopwordlist:
            if len(word)>1:
                # Lemmatizing the word.
                word = wordLemm.lemmatize(word)
                tweetwords += (word+' ')

        processedText.append(tweetwords)

    return processedText

processedtext = preprocess(text)

processedtext

"""# 2.1. Data Visualisation

## 2.1.1 Word Cloud
"""

pos_tweet = processedtext[800000:]
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800, background_color = "white",
              collocations=False).generate(" ".join(pos_tweet))
plt.figure(figsize = (20,20))
plt.imshow(wc)
wc.to_file('Positive Tweets Word Cloud.png')

neg_tweet = processedtext[:800000]
plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800, background_color = "white",
               collocations=False).generate(" ".join(neg_tweet))
plt.imshow(wc)
wc.to_file('Negative Tweets Word Cloud.png')

"""# 3.0 Machine Learning Approach"""

# Labelling Dataset
X = processedtext
y = sentiment

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

#TF-IDF
tfidf_vectorizer = TfidfVectorizer(use_idf=True)
X_train_vectors_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_vectors_tfidf = tfidf_vectorizer.transform(X_test)

scikit_log_reg = LogisticRegression(verbose=1, solver='liblinear',random_state=0, C=5, penalty='l2',max_iter=1000)
model_LR=scikit_log_reg.fit(X_train_vectors_tfidf,y_train)
lr_predicted= model_LR.predict(X_test_vectors_tfidf)
print("Logistic Regression with TFIDF:",metrics.accuracy_score(y_test, lr_predicted))

from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
# Classification Report
print(classification_report(y_test,lr_predicted))
