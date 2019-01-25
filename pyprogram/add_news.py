#! python3
# coding=UTF-8

def add_word(Client_IP):#增加辭典
    with open('./all_dict/繁體中文詞庫.txt', 'r', encoding='utf-8') as new_dict :#
        new_word = new_dict.readlines()

    

    with open('./all_dict/user_news.txt', 'r', encoding='utf-8') as news_f :
        news_user  = news_f.readlines()
        for word in news_user:
            if word not in new_word:
                new_word.append(word)

    new_dict = open('./all_dict_user/'+Client_IP+'/new_dict.txt', 'a', encoding='utf-8')
    new_dict.write('\n')
    for word in new_word:
        if '\n' in word:
            new_dict.write(word)
        else:
            new_dict.write(word+'\n')
    new_dict.close()

import sys

Client_IP = str(sys.argv[1])

add_word(Client_IP)

