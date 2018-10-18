def add_word():#增加辭典
    new_f = open('../all_dict/new_words.txt', 'r', encoding='utf-8')
    new_word2 = new_f.readlines()
    with open('../all_dict/繁體中文詞庫.txt', 'r', encoding='utf-8') as new_dict :#
        new_word = new_dict.readlines()
        for i in new_word2:
            if i not in new_word:
                new_word.append(i)

    new_f.close()
    new_dict = open('../all_dict/new_dict.txt', 'w', encoding='utf-8')
    for word in new_word:
        if '\n' in word:
            new_dict.write(word)
        else:
            new_dict.write(word+'\n')
    new_dict.close()

add_word()