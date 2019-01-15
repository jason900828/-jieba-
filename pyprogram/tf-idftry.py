#! python3
# coding=UTF-8
"""
Created on Mon Oct  8 13:39:54 2018

@author: rayzhan34
"""
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
import time
import sys
import json
import csv
def delect_Stopword(Folder_name):

    #StopWord_combine()
    stpwrdpath = "all_dict_user/"+Folder_name+"/all_stop.txt"
    stpwrd_dic = open(stpwrdpath, 'r',encoding = 'utf-8')
    stpwrdlst = stpwrd_dic.read().replace('\n', ' ').split()#將停用詞表轉換為list 
    stpwrd_dic.close()#將文本中的詞語轉換為詞頻矩陣，矩陣元素a[i][j] 表示j詞在i類文本下的詞頻 

    new_corpus = []
    
    stpwrdlst_n = []
    for stop in stpwrdlst:
        stop = stop.replace('\n','')
        stpwrdlst_n.append(stop)
    
    return stpwrdlst_n
starttime = time.time()

Folder_name = sys.argv[1]#sys.argv[1]# #讀斷完詞後的資料夾編號，平常測試要將此改掉
rank = int(sys.argv[2])
dotfidf = int(sys.argv[3])

path = './cut_over/cut'+str(Folder_name)+'/'
file_name = os.listdir(path)

corpus = []
corpus_speech = []
for doc in file_name:            
    with open(path+doc,'r',encoding = 'utf-8') as f:
        file_json = f.read()
        file_lst = json.loads(file_json)
        corpus_dict = {}
        for word in file_lst:
            corpus_dict[word[0]] = word[1]
        corpus_speech.append(corpus_dict)
        file_str = ''
        with open(path+'content.txt','w',encoding = 'utf-8') as f:
            for w in file_lst:
                f.write(w[0]+' ')
        with open(path+'content.txt','r',encoding = 'utf-8') as f:
            file_str = f.read()

    corpus.append(file_str)

stpwrdlst_n = delect_Stopword(str(Folder_name))
vectorizer = CountVectorizer(stop_words = stpwrdlst_n)#創建詞袋數據結構#創建hash向量詞袋# 
#vectorizer = HashingVectorizer(stop_words =stpwrdlst,n_features = 1000)#設置停用詞詞表
tf = vectorizer.fit_transform(corpus)
words=vectorizer.get_feature_names()#获取词袋模型中的所有词语 
tf_weight=tf.toarray()

if dotfidf:
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(tf)#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵    
    tfidf_weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重 
fn = 0
path = './keyword/keyword'+str(Folder_name)+'/'

if not os.path.isdir('./keyword'):
    os.mkdir('./keyword')
if not os.path.isdir(path):
    os.mkdir(path)


if dotfidf:
    with open(path+'keyword.csv', 'w', newline='',encoding = 'big5') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入一列資料
        writer.writerow(['word','TF','IDF','TF-IDF(原始)', 'TF-IDF(標準化)','詞性','分類'])
        for  w in range(len(tfidf_weight)):
            
            loc = np.argsort(-tfidf_weight[w])
            corpus_speech_keys = corpus_speech[fn].keys()
            for r in range(rank):
                if tfidf_weight[w][loc[r]] ==0.0:
                    break
                    # 寫入另外幾列資料
                tf_n = round(tf_weight[w][loc[r]]/len(corpus_speech[w]),4)
                idf_n = round(transformer.idf_[loc[r]],4)
                tfidf_n = round(tf_n*idf_n,4)
                if words[loc[r]] in corpus_speech_keys :
                    speech = corpus_speech[fn][words[loc[r]]]
                else:
                    speech = 'x'
                category = file_name[fn].replace('.json','')
                try:
                    writer.writerow([words[loc[r]],tf_n,idf_n,tfidf_n,round(tfidf_weight[w][loc[r]],4),speech,category])
                except:
                    print('有字元無法用big5編碼<br/>')
            fn+=1
else:
    with open(path+'keyword.csv', 'w', newline='',encoding = 'big5') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入一列資料
        writer.writerow(['word','TF','IDF','TF-IDF(原始)', 'TF-IDF(標準化)','詞性','分類'])
        for  w in range(len(tf_weight)):
        
            
            loc = np.argsort(-tf_weight[w])
            corpus_speech_keys = corpus_speech[fn].keys()
            if len(tf_weight)<1 or len(tf_weight)==1:
                category = 'null'
            else:
                category = file_name[fn].replace('.json','')
            for r in range(len(tf_weight[w])):
                if tf_weight[w][loc[r]] == 0:
                    break
                tf_n = round(tf_weight[w][loc[r]]/len(corpus_speech[w]),4)
                
                if words[loc[r]] in corpus_speech_keys :
                    speech = corpus_speech[fn][words[loc[r]]]
                else:
                    speech = 'x'
                
                
                try:
                    writer.writerow([words[loc[r]],tf_n,'null','null','null',speech,category])
                    
                except:
                    print('有字元無法用big5編碼<br/>')
                    
            fn+=1
file = './cut_over/cut'+str(Folder_name)+'/content.txt'
os.remove(file)
endtime = time.time()
#print("end<br/>")

print("tf-idf cost : "+str(endtime-starttime)+"<br/>")