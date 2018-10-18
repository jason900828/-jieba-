coding = 'utf-8'
import math
import jieba
import logging
#from hanziconv import HanziConv
#from langconv import * #簡轉繁套件
import os
import sys 
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import HashingVectorizer
import time
import jieba.analyse
import zipfile
import re

'''def Simp2Trad(in_files,index,size):
    #将简体转换成繁体

    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    with open(in_files,'r',encoding='utf-8') as f:
        change = f.readlines()
    
    #texts_num = 0
    #print(len(change))
    print('task {0} Running'.format(index))
    size = math.ceil(len(change)/size)
    start = size*index
    end = (index+1)*size if(index+1)*size<len(change) else len(change)
    temp_data = change[start:end]
    
    output = []
    t1 = time.time()
    for num, temp in enumerate(temp_data):
        temp = Converter('zh-hant').convert(temp)
        output.append(text)
        if (num+1)%10000 == 0:
            print('task {0} 已轉換 {1} '.format(index,num+1))
            
    t2 = time.time()
    print('HanziConv {0} : {1}'.format(index,t2-t1))

    return output
'''
        
    
def get_data(Folder_name):##提取data，文本路徑放置在data資料夾裡，單文本多文本皆可，單文本必須為txt，編碼為utf-8，多文本必須為zip檔打包在一起，同樣需要utf-8編碼
    
    path = './data/'+str(Folder_name)+'/'
    
    file_format = os.listdir(path)
    txt_long = []
    #print(path+str(file_format[0]+'<br/>'))
    if '.txt' in file_format[0]:#單文本讀取
        with open(path+file_format[0], 'r', encoding='utf-8') as content :
            data_str = content.read()
            
            results=re.findall(r'http://[a-zA-Z0-9.?/&=:]*',data_str)#去除url
            for url in results:
                data_str = data_str.replace(url,'')

                #print(url)
            results=re.findall(r'https://[a-zA-Z0-9.?/&=:]*',data_str)#去除url
            for url in results:
                data_str = data_str.replace(url,'')
                #print(url)
            data_lst = data_str.split('\n')       #之後需要跑多進程，故將文本切開之後儲存在list好做檔案切割
            data = []
            for words in data_lst:
                if words == '' or words == '\n':
                    continue
                else:
                    data.append(words)
            print(path+file_format[0]+" already loaded"+"<br/>")

    elif '.zip' in file_format[0]:#多文本讀取
        #print(path+str(file_format[0]+'<br/>'))
        azip = zipfile.ZipFile(path+file_format[0])
        a_lst = azip.namelist()
        #print(a_lst)
        data = []
        if len(a_lst)<4:#zip檔小於4個文本，將所有文本合在一起再分類
            
            data_lst = []
            for i in a_lst:
                data_str = azip.read(i).decode('utf-8')
                results=re.findall(r'http://[a-zA-Z0-9.?/&=:]*',data_str)#去除url
                for url in results:
                    data_str = data_str.replace(url,'')
                    #print(url)
                results=re.findall(r'https://[a-zA-Z0-9.?/&=:]*',data_str)#去除url
                for url in results:
                    data_str = data_str.replace(url,'') 
                    #print(url)  
                data_lst = data_str.split('\n')#之後需要跑多進程，故將文本切開之後儲存在list好做檔案切割
                for str_ in data_lst:
                    if str_  == '' or str_ == '\n':
                        continue
                    data.append(str_)
                txt_long.append(len(data))
                
            print(path+file_format[0]+" already loaded,doc number : "+str(len(a_lst))+"<br/>")
        else :#zip檔大於4個文本，直接讀取每一個文本
            for i in a_lst:
                data_str = azip.read(i).decode('utf-8')
                results=re.findall(r'http://[a-zA-Z0-9.?/&=:]*',data_str)#去除url
                for url in results:
                    data_str = data_str.replace(url,'')
                    #print(url)
                results=re.findall(r'https://[a-zA-Z0-9.?/&=:]*',data_str)#去除url
                for url in results:
                    data_str = data_str.replace(url,'') 
                    #print(url)
                data_str = data_str.replace('\n','')
                data.append(data_str)#不須切割，因為文本數量很多，直接儲存在list分割
                
            print(path+file_format[0]+" already loaded,doc number : "+str(len(a_lst))+"<br/>")

    return data,txt_long,file_format[0]


def store_data(path,txt_long_lst,file_format,data):

    if os.path.isdir(path):
        del_ = os.listdir(path)
        for d in del_:
            os.remove(path+d)

        os.removedirs(path)

    if not os.path.isdir('cut_over/'):
        os.mkdir('cut_over/')

    if not os.path.isdir(path):
        os.mkdir(path)
    

    if '.txt' in file_format: #單文本儲存
        with open(path + file_format, 'w', encoding = 'utf-8') as output:
            for words in data:

                output.write(words+'\n')
        print(path + file_format + " already saved<br/>")

    else:  #多文本儲存
        if len(txt_long_lst) == 0:#如果txt_long_lst裡面為空值，代表文本數超過4個，故儲存方法不同
            k = 0
            for doc in data:
                '''if k == 0:#ZipFile讀出檔名第一個為資料夾，故跳過第一個
                    k += 1
                    continue'''
                output = open(path+str(k)+'.txt', 'w', encoding = 'utf-8')
                output.write(doc)
                output.close()
                k += 1
            print(path+file_format+" already saved,doc number : "+str(len(data))+"<br/>")

        else:#txt_long_lst不為空值，故抓取每個文章長度
            k = 0 
            start = 0
            for i in txt_long_lst:
                '''if k == 0:#ZipFile讀出檔名第一個為資料夾，故跳過第一個
                    k += 1
                    continue'''
                output = open(path+str(k)+'.txt', 'w', encoding = 'utf-8')
                for j in range(start,i,1):#逐行儲存，一直到與紀錄長度相等
                    output.write(data[j])
                start = i
                output.close()
                k += 1
            print(path+file_format+" already saved,doc number : "+str(len(txt_long_lst))+"<br/>")




def cut(content,index,size):#斷詞
    jieba.set_dictionary('all_dict\\dict.txt.big') #繁體簡體皆有
    
    #jieba.load_userdict('all_dict\\new_dict.txt')#自行擴充的辭庫
    
    #print('task {0} Running <br/>'.format(index))
    size = math.ceil(len(content)/size) #跑多進程  所以將資料切成四份(cpu 4 核心)分別處理
    start = size*index
    end = (index+1)*size if(index+1)*size<len(content) else len(content)
    temp_data = content[start:end]

    word = []
    for num,temp in enumerate(temp_data):
        word.append(' '.join(jieba.cut(temp)))
        if (num + 1) % 10000 == 0:
            logging.info("task %d 已完成前 %d 行的斷詞" % (index,num + 1))
    
    #print('task {0} end<br/>'.format(index))
    return word

'''
def Corpus_delect_Stopword(corpus):

    #StopWord_combine()
    stpwrdpath = "all_dict\\all_stop.txt"
    stpwrd_dic = open(stpwrdpath, 'r',encoding = 'utf-8')
    stpwrdlst = stpwrd_dic.readlines()#將停用詞表轉換為list 
    stpwrd_dic.close()#將文本中的詞語轉換為詞頻矩陣，矩陣元素a[i][j] 表示j詞在i類文本下的詞頻 

    new_corpus = []
    
    stpwrdlst_n = []
    for stop in stpwrdlst:
        stop = stop.replace('\n','')
        stpwrdlst_n.append(stop)
    #print(stpwrdlst_n)
    for content in corpus:
        new_content = ''
        
        for word in content.split():
            
            if word  not in stpwrdlst_n:
                #print(word)
                new_content = new_content + word + ' '
        new_corpus.append(new_content)
    return new_corpus
    
def delect_Stopword():

    #StopWord_combine()
    stpwrdpath = "all_dict\\all_stop.txt"
    stpwrd_dic = open(stpwrdpath, 'r',encoding = 'utf-8')
    stpwrdlst = stpwrd_dic.readlines()#將停用詞表轉換為list 
    stpwrd_dic.close()#將文本中的詞語轉換為詞頻矩陣，矩陣元素a[i][j] 表示j詞在i類文本下的詞頻 

    new_corpus = []
    
    stpwrdlst_n = []
    for stop in stpwrdlst:
        stop = stop.replace('\n','')
        stpwrdlst_n.append(stop)
    
    return stpwrdlst_n  



def tf_idf(corpus):

    #corpus = Corpus_delect_Stopword(corpus)
    stpwrdlst_n = delect_Stopword()


    vectorizer = CountVectorizer(stop_words = stpwrdlst_n)#創建詞袋數據結構#創建hash向量詞袋# 
    #vectorizer = HashingVectorizer(stop_words =stpwrdlst,n_features = 1000)#設置停用詞詞表

    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵    
    
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语    
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重 

    return word,weight
    '''