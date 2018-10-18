<?php

header("Content-Type:text/html; charset=utf-8");

require_once(dirname(__FILE__) . "/config.php");

#計算時間的涵式
function exec_time($timeN,$timeP){
    $time = strtotime($timeN) - strtotime($timeP); 
    $n_time = str_pad(floor($time/3600/24),2,0,STR_PAD_LEFT )."天".str_pad(floor($time%(24*3600)/3600),2,0,STR_PAD_LEFT )."小時".str_pad(floor($time%3600/60),2,0,STR_PAD_LEFT)."分".str_pad($time%3600%60, 2, 0, STR_PAD_LEFT)."秒";
    return $n_time;
}

$timenamefolder=date("YmdHis").rand(0,100);#製作多個使用者時的分辨用資料夾，以時間與亂數0~100為命名規則
$time1=date("Y-m-d H:i:s");#上傳開始時間

$uploadhtm = 'index.html';
$uploaddir = './data/'.$timenamefolder.'/';//儲存路徑

if (!file_exists($uploaddir)){
    mkdir($uploaddir);

    }
else{
    return;
}


# 檢查檔案是否上傳成功
if ($_FILES['my_file']['error'] === UPLOAD_ERR_OK){
  echo '檔案名稱: ' . $_FILES['my_file']['name'] . '<br/>';
  echo '檔案類型: ' . $_FILES['my_file']['type'] . '<br/>';
  echo '檔案大小: ' . ($_FILES['my_file']['size'] / 1024) . ' KB<br/>';
  echo '暫存名稱: ' . $_FILES['my_file']['tmp_name'] . '<br/>';

  # 檢查檔案是否已經存在
  if (file_exists($uploaddir. $_FILES['my_file']['name'])){
    echo '檔案已存在。<br/>';
  } else {
    $file = $_FILES['my_file']['tmp_name'];
    $dest = $uploaddir . $_FILES['my_file']['name'];
    

    # 將檔案移至指定位置
    rename($file, $dest);
    
  }
} else {
  echo '錯誤代碼：' . $_FILES['my_file']['error'] . '<br/>';
}
$time2 = date("Y-m-d H:i:s");
/*if (!file_exists('./export/'.$timenamefolder)){
  mkdir('./export/'.$timenamefolder);
}*/
// $output=shell_exec("/usr/local/bin/python3 tokens.py $timenamefolder $filename");#macOS呼叫與傳值給python
echo shell_exec("python ./pyprogram/jieba-mutliprocessing.py $timenamefolder");#Windows系統呼叫與傳值給python

if($_POST["tfidf"] == '1'){
  echo shell_exec("python ./pyprogram/tf-idftry.py $timenamefolder");
}

else{
  echo $_POST["tfidf"]."沒有跑tf-idf<br/>";
}

$time3 = date("Y-m-d H:i:s");
echo '開始時間'.$time1.'<br />';
echo '上傳時間統計：'.exec_time($time2,$time1).'<br />';
echo '分詞時間統計：'.exec_time($time3,$time2).'<br />';
echo '總執行時間：'.exec_time($time3,$time1).'<br />';
echo '<br />'."<button type=\"button\" onclick=\"location.href='./phpdownload/downloadcut.php?id=".$timenamefolder."'\">下載斷詞</button>".'<br />'.'<br />';
        

if($_POST["tfidf"] == '1'){   
    echo "<button type=\"button\" onclick=\"location.href='./phpdownload/downloadTF-IDF.php?id=$timenamefolder'\"> 下載TF-IDF</button>".'<br />'.'<br />';

    echo "<button type=\"button\" onclick=\"location.href='./phpdownload/downloadkeyword.php?id=$timenamefolder'\"> 下載keyword</button>".'<br />';
}
  

    

?>
