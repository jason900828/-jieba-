#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:39:54 2018

@author: rayzhan34
"""


import time
#輸入套件
import os
import sys
#要注意txt是否是OS x 可以支援的
#txt改完變成utf8後就不能再打開了
corpus = []


######去除停用詞跟斷詞
#print("start<br/>")
starttime = time.time()
stopword = []
with open('./all_dict/all_stop.txt','r',encoding = 'utf-8') as f:
    for line in f:
        line = line.strip('\n')
        if line != '':
            stopword.append(line)
            
Folder_name = sys.argv[1]  

path = './cut_over/cut'+str(Folder_name)+'/'
file_name = os.listdir(path)

test = []
for doc in file_name:            
    with open(path+doc,'r',encoding = 'utf-8') as f:
        test_str = '' 
        for sen in f.readlines():
            if sen == '\n':
                continue
            else:
                test_str = test_str + sen
    test_lst1 = test_str.split(' ')
    test_lst2 = []
    for wor in test_lst1:
        if wor == '':
            continue
        else:
            test_lst2.append(wor)#4秒
    test.append(test_lst2)
    

#remainderWords = list(filter(lambda a: a not in stopword , test))#很多時間
hash_dict = {}
total_lst = []
doc_count = 0
for t_lst in test:
    hash_ = {}
    for item in t_lst:
        if item.strip('\n') in hash_:
            hash_[item.strip('\n')] +=1
        else:
            hash_[item.strip('\n')] = 1
         
    for stop in stopword:
        try:
            del hash_[stop]
            #print(stop)
        except:
            continue
    keyword = hash_.keys()
    key_del = []
    for k in keyword:
        if len(k)<2:
            key_del.append(k)   
    for k in key_del:
        del hash_[k]
        
    hash_dict[doc_count] = hash_
    doc_count+=1
    total = 0
    keyword = hash_.keys()
    for k in keyword:
        total = total + hash_[k]
    total_lst.append(total)
    

#自建tfidf函數
import math
import string
from collections import Counter
from nltk.stem.porter import *

#count = Counter(test)

#print(count)
#print(count.most_common(10))



def tf(count,total):
    return count/total
def n_containing(word,count_list):
    #print(sum(1 for count in count_list if word in count))
    
    return sum(1 for count in count_list if word in str(count))
def idf(word,count_list):
    return math.log(len(count_list)/(1+n_containing(word,count_list)),10)
#因為照原公式算出來的tf-idf值大多在小數點第二位以下，因此加權一萬以方便比較
def tfidf(word,count,count_list,total):
    return tf(count,total) * idf(word,count_list) * 100


#count1 = list(hash_) 

#print(len(count1))
i = 0
#print(hash_lst[0])
#print("\n\n\n\n\n")
#print(hash_lst[1])
path = 'keyword/keyword'+str(Folder_name)+'/'
if os.path.isdir(path):
    del_ = os.listdir(path)
    for d in del_:
        os.remove(path+d)
    os.removedirs(path)
if not os.path.isdir('keyword/'):
    os.mkdir('keyword/')
if not os.path.isdir(path):
    os.mkdir(path)
keyword_f = open(path+'keyword-by-tf_idf.txt', 'w',encoding = 'utf-8')

path = './tf-idf/tf-idf'+str(Folder_name)+'/'
if os.path.isdir(path):
    del_ = os.listdir(path)
    for d in del_:
        os.remove(path+d)
    os.removedirs(path)
if not os.path.isdir('tf-idf/'):
    os.mkdir('tf-idf/')
if not os.path.isdir(path):
    os.mkdir(path)
tf_idf_f = open(path+'tf_idf.txt', 'w', encoding='utf-8')


for i in range(doc_count):
    scores = {}
    
    
    for word in hash_dict[i].keys():
        a = tfidf(word,hash_dict[i][word],hash_dict,total_lst[i])
        scores.update({word:a})
    
    
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    keyword_f.write("Top words in document "+str(i)+"\n")
    for word, score in sorted_words[:5]:
        keyword_f.write("Word: {}, TF-IDF: {}\n".format(word, round(score, 5)))
    tf_idf_f.write("Top words in document "+str(i)+"\n")
    for word, score in sorted_words:
        tf_idf_f.write("Word: {}, TF-IDF: {}\n".format(word, round(score, 5)))
    i+=1

keyword_f.close()
tf_idf_f.close()
endtime = time.time()
#print("end<br/>")
print("tf-idf cost : "+str(endtime-starttime)+"<br/>")