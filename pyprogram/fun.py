#! python3
# coding=UTF-8
import math
import json
import jieba
import jieba.posseg as pseg
#from hanziconv import HanziConv
#from langconv import * #簡轉繁套件
import os
import sys 
from pathlib import Path
#from sklearn import feature_extraction
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import HashingVectorizer
import time
#import jieba.analyse
import xlrd
import zipfile36 as zipfile
import re
import pandas as pd
import csv
import logging

def get_data(Folder_name,excel_where_category,excel_where_content_at):###提取data，文本路徑放置在data資料夾裡，單文本多文本皆可，單文本必須為txt，編碼為utf-8，多文本必須為zip檔打包在一起，或是excel，同樣需要utf-8編碼
    
    path = './data/'+str(Folder_name)+'/'
    
    file_format = os.listdir(path)
    txt_long = []
    fn_lst = []
    #print(path+str(file_format[0]+'<br/>'))
    if '.txt' in file_format[0]:#單文本讀取
        with open(path+file_format[0], 'r', encoding='utf-8') as content :
            data_str = content.read()
            data_lst = data_str.split('\n')       #之後需要跑多進程，故將文本切開之後儲存在list好做檔案切割
            data = []
            for words in data_lst:
                if words == '' or words == '\n':
                    continue
                else:
                    data.append(words)
            print("already loaded"+"<br/>")

    elif '.zip' in file_format[0]:#多文本讀取
        #print(path+str(file_format[0]+'<br/>'))
        azip = zipfile.ZipFile(path+file_format[0], 'r')
        
        a_lst = azip.namelist()
        fn_lst = []
        for fn in a_lst:
            right_fn = fn.encode('cp437').decode('ansi')
            fn_lst.append(right_fn)

        data = []
        for i in a_lst:
            data_str = azip.read(i).decode('utf-8')   
            data_str = data_str.replace('\n','')
            data.append(data_str)
                
        print("already loaded,doc number : "+str(len(a_lst))+"<br/>")
    elif '.xlsx' in file_format[0]:

        data = []
        excel_category = []
        wb = xlrd.open_workbook(path+file_format[0])
        sheets = wb.sheet_names()
        
        if '/' in excel_where_category[0]:
            excel_where_category = excel_where_category[0].split('/')
        else:
            excel_where_category.append(excel_where_category[0])
            excel_where_category[0] = sheets[0]
        if '/' in excel_where_content_at[0]:
            excel_where_content_at = excel_where_content_at[0].split('/')
        else:
            excel_where_content_at.append(excel_where_content_at[0])
            excel_where_content_at[0] = sheets[0]



        
        df1 = pd.read_excel(path+file_format[0], sheet_name=excel_where_category[0])
        df1 = df1.fillna(value = "<NAN>")
        df2 = pd.read_excel(path+file_format[0], sheet_name=excel_where_content_at[0])
        df2 = df2.fillna(value = "<NAN>")
        for i in range(len(df2)):
            if excel_where_category[1] == 'no-excel':
                if df2[excel_where_content_at[1]][i] != "<NAN>":#去除掉是空值(NAN)的格子
                    data.append(str(df2[excel_where_content_at[1]][i]))
                    txt_long.append(i)
            elif df1[excel_where_category[1]][i] in excel_category :
                if df2[excel_where_content_at[1]][i] != "<NAN>":#去除掉是空值(NAN)的格子
                    category_index = excel_category.index(str(df1[excel_where_category[1]][i]))
                    data[category_index] = data[category_index] +'\n'+ str(df2[excel_where_content_at[1]][i])#新增文章
            else:
                if df2[excel_where_content_at[1]][i] != "<NAN>":
                    excel_category.append(str(df1[excel_where_category[1]][i]))#新增分類
                    data.append(str(df2[excel_where_content_at[1]][i]))
                txt_long = excel_category
        for i in range(len(txt_long)):#替換掉分類中有非法命名的字元
            txt_long[i] = str(txt_long[i]).replace('/','_')
            txt_long[i] = str(txt_long[i]).replace('\\','_')
            txt_long[i] = str(txt_long[i]).replace(':','_')
            txt_long[i] = str(txt_long[i]).replace('*','_')
            txt_long[i] = str(txt_long[i]).replace('?','_')
            txt_long[i] = str(txt_long[i]).replace('"','_')
            txt_long[i] = str(txt_long[i]).replace('<','_')
            txt_long[i] = str(txt_long[i]).replace('>','_')
            txt_long[i] = str(txt_long[i]).replace('|','_')


    return data,txt_long,file_format[0],fn_lst


def store_data(path,txt_long_lst,file_format,data,fn_lst):

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
        store_data = []
        for sentence in data:
            for word in sentence:
                store_data.append(word)
 
        with open(path + file_format.replace('.txt','.json'), 'w', encoding = 'utf-8') as output:
            json.dump(store_data,output,ensure_ascii=False)
        print(" already saved txt<br/>")

    elif'.xlsx' in file_format:
        for i in range(len(txt_long_lst)):
            with open(path + str(txt_long_lst[i]) + '.json', 'w', encoding = 'utf-8') as output:
                json.dump(data[i],output,ensure_ascii=False)
        print(" already saved xlsx<br/>")
    
    else:  #多文本儲存
        if '.txt' not in fn_lst[0]:
            for fn in range(1,len(fn_lst)):
                fn_lst[fn] = fn_lst[fn].replace(fn_lst[0],'')
            fn_lst[0] = 'first.txt'
        if len(txt_long_lst) == 0:#如果txt_long_lst裡面為空值，代表文本數超過4個，故儲存方法不同
            for k in range(len(fn_lst)):
                if fn_lst[k] == 'first.txt':
                    continue
                output = open(path+fn_lst[k].replace('.txt','.json'), 'w', encoding = 'utf-8')
                json.dump(data[k],output,ensure_ascii=False)
                output.close()
            print(" already saved,doc number : "+str(len(fn_lst))+"<br/>")

def cut(content,index,size,Folder_name):#斷詞
    jieba.set_dictionary('./all_dict/dict.txt.big') #繁體簡體皆有
    
    jieba.load_userdict('./all_dict_user/'+str(Folder_name)+'/new_dict.txt')#自行擴充的辭庫
    
    #print('task {0} Running <br/>'.format(index))
    size = math.ceil(len(content)/size) #跑多進程  所以將資料切成四份(cpu 4 核心)分別處理
    start = size*index
    end = (index+1)*size if(index+1)*size<len(content) else len(content)
    temp_data = content[start:end]

    data = []
    temp_data = clean_url(temp_data)
    for num,temp in enumerate(temp_data):
        word = pseg.cut(temp)
        sentence = []
        for w in word:
            sentence.append([w.word,w.flag])
        data.append(sentence)
        if num%1000==0:
            logging.info('已完成 '+str(num))
    #print(time1-time0)
    #print('task {0} end<br/>'.format(index))
    return data

def clean_url(temp_data):#清理url
    for i in range(len(temp_data)):
        results=re.compile(r'http://[a-zA-Z0-9;/?:@&=+.]*',re.S)
        temp_data[i]=results.sub("",temp_data[i])
        results=re.compile(r'https://[a-zA-Z0-9;/?:@&=+.]*',re.S)
        temp_data[i]=results.sub("",temp_data[i])
    #print(time1-time0)
    return temp_data

