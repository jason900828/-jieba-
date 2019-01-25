#! python3
# coding=UTF-8
def StopWord_combine(Client_IP):#將原本的stopword加上使用者不想看到的word

    with open('./all_dict/ch_stop.txt', 'r', encoding='utf-8') as stop_f :
        stop_word  = stop_f.readlines()
    with open('./all_dict/user_stop.txt', 'r', encoding='utf-8') as stop_f :
        stop_user  = stop_f.readlines()
        for word in stop_user:
            if word not in stop_word:
                stop_word.append(word)

    with open('./all_dict_user/'+Client_IP+'/all_stop.txt', 'a', encoding='utf-8') as all_stop_f :
        all_stop_f.write('\n')
        for word in stop_word:
            if '\n' in word:
                all_stop_f.write(word)
            else:
                all_stop_f.write(word+'\n')

import sys
Client_IP = str(sys.argv[1])
StopWord_combine(Client_IP)
