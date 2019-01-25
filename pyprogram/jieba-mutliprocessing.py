#! python3
# coding=UTF-8

from os import listdir
import time
from fun import cut,get_data,store_data#,add_word
import multiprocessing as mp
import os
import sys
import json

if __name__ == '__main__':
    #t1 = time.time()
    
    #jieba.set_dictionary('all_dict\\dict.txt.big')
    #jieba.load_userdict('all_dict\\繁體中文詞庫.txt')
    """
    output = open('cut_over.txt', 'w', encoding='utf-8')
    with open('data.txt', 'r', encoding='utf-8') as content :
        for texts_num, line in enumerate(content):
            line = line.strip('\n')
            words = jieba.cut(line, cut_all=False)
            for word in words:
                output.write(word + '/')
            output.write('\n')

            if (texts_num + 1) % 10000 == 0:
                logging.info("已完成前 %d 行的斷詞" % (texts_num + 1))
    output.close()
    
    t2 = time.time()
    t_cost = t2-t1
    
    print('cost time : '+str(t_cost))
    #上方程式碼為斷詞單進程
    大約要61分鐘
    """
    t3 = time.time()
    
    
    Folder_name = sys.argv[1]#2018101510141823
    f = open('./all_dict_user/'+str(Folder_name)+'/excel_category.json','r',encoding = 'utf-8')
    jsondata = json.loads(f.read())
    excel_where_category =[jsondata['excel_category']]
    excel_where_content_at = [jsondata['excel_content']]
    f.close()
    print("python:<br/>")
    
    
    cuts,txt_long_lst,file_format,fn_lst = get_data(Folder_name,excel_where_category,excel_where_content_at)#e,
    #add_word()#新增使用者想要的詞彙
    mod_list = []
    t4 = time.time()
    print("start MP:"+str(t4-t3)+"<br/>")
    
    #print('wait parallel cut word<br/>')
    if (len(cuts)>1) and (len(cuts)<mp.cpu_count()):
        processor = len(cuts)
    else:
        processor = mp.cpu_count()
    
    

    p = mp.Pool()
    
    for i in range(processor):
        mod_list.append(p.apply_async(cut, args = (cuts,i,processor,Folder_name,)))

    p.close()
    p.join()
    #print('done...<br/>')
    data = []
    for mod in mod_list:
        exp = mod.get()
        for i in exp:
            data.append(i)
    
    path = './cut_over/cut'+str(Folder_name)+'/'

    store_data(path,txt_long_lst,file_format,data,fn_lst)
    
    #w = p.map(cut_cword,contenti,processor)
    
    t4 = time.time()
    t_cost2 = t4-t3    
    print('parallel cost2 time : '+str(t_cost2)+'<br/>')
    #斷詞多進程
    #執行時間約25分鐘

    '''
    print('簡體轉繁體中文....')#大約15分鐘，hanziconv 錯字一堆
    output = open('data.txt', 'w', encoding='utf-8')
    processor = mp.cpu_count()
    p = mp.Pool()
    mod_list = []
    for i in range(processor):
            mod_list.append(p.apply_async(Simp2Trad, args = ('cut_over.txt',i,processor,)))
    p.close()
    p.join()

    for mod in mod_list:
        Traditional = mod.get()
        #print(wo)
        for tr in Traditional:
            output.write(tr)
    output.close()

    print("完成...")
    '''