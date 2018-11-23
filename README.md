# -分詞系統(基於jieba)-
*upload.php與calltf-idf.php內有呼叫python腳本的命令，可以依照需求更改命令

*exec命令範例：'python ./pyprogram/jieba-mutliprocessing.py '.$timenamefolder

打開index.html
依照上面的步驟上傳檔案並設定停止詞跟新增詞


實測檔案

4.6MB單一文檔                花費15秒

5.7MB兩個文檔  沒有跑TF-IDF   花費16秒

5.7MB兩個文檔  有跑TF-IDF     花費19秒

33.4MB六個文檔 有跑TF-IDF     花費1分42秒

123MB三百八十四個文檔  有跑TF-IDF     花費18分24秒

使用語言:HTML、JavaScript、jQuery、CSS、PHP、Python
