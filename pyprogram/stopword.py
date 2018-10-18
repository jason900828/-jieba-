def del_word():#新增停用詞
    del_list = []
    with open('../all_dict/del_words.txt', 'r', encoding='utf-8') as del_f :
        del_list = del_f.readlines()
    return del_list

    
def StopWord_combine():#將原本的stopword加上使用者不想看到的word

    with open('../all_dict/ch_stop.txt', 'r', encoding='utf-8') as stop_f :
        stop_word  = stop_f.readlines()

    ne_del = del_word()
    for temp_stop in ne_del:
        stop_word.append(temp_stop)

    with open('../all_dict/all_stop.txt', 'w', encoding='utf-8') as all_stop_f :
        for word in stop_word:
            if '\n' in word:
                all_stop_f.write(word)
            else:
                all_stop_f.write(word+'\n')
            
StopWord_combine()