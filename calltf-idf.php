<?php

header("Content-Type:text/html; charset=utf-8");

require_once(dirname(__FILE__) . "/config.php");

#計算時間的涵式

function exec_time($timeN,$timeP){
    $time = strtotime($timeN) - strtotime($timeP); 
    $n_time = str_pad(floor($time/3600/24),2,0,STR_PAD_LEFT )."天".str_pad(floor($time%(24*3600)/3600),2,0,STR_PAD_LEFT )."小時".str_pad(floor($time%3600/60),2,0,STR_PAD_LEFT)."分".str_pad($time%3600%60, 2, 0, STR_PAD_LEFT)."秒";
    return $n_time;
}

function uploadfile($file_id,$uploaddir,$file_name){

  if (!file_exists($uploaddir)){
    mkdir($uploaddir);
  }
  if ($_FILES[$file_id]['error'] === UPLOAD_ERR_OK){

    # 檢查檔案是否已經存在
    if (file_exists($uploaddir . $file_name)){
      unlink($uploaddir . $file_name);
      echo "已刪除";
    } 
    $file = $_FILES[$file_id]['tmp_name'];
    $dest = $uploaddir . $file_name;
    # 將檔案移至指定位置
    rename($file, $dest);
    
  } else {
   echo '錯誤代碼：' . $_FILES[$file_id]['error'] . '<br/>';

  }
}



//$timenamefolder = GetIP();#製作多個使用者時的分辨用資料夾，以時間與亂數0~100為命名規則
//if(!$timenamefolder){
$timenamefolder=$_POST["id_number"];

echo 
uploadfile('del_file','./all_dict_user/'.$timenamefolder.'/','all_stop.txt');



include("./phpadddict/add_del.php");
echo Do_del($timenamefolder,$_POST["del_word"]);

$time1=date("Y-m-d H:i:s");#上傳開始時間

$uploadhtm = 'index.html';
$uploaddir = './data/'.$timenamefolder.'/';//儲存路徑



/*if (!file_exists('./export/'.$timenamefolder)){
  mkdir('./export/'.$timenamefolder);
}*/
// $output=shell_exec("/usr/local/bin/python3 tokens.py $timenamefolder $filename");#macOS呼叫與傳值給python





echo exec("python ./pyprogram/tf-idftry.py ".$timenamefolder." ".$_POST["tfidf_rank"]." 1",$array, $ret);


$time3 = date("Y-m-d H:i:s");
echo '開始時間'.$time1.'<br />';
echo '總執行時間：'.exec_time($time3,$time1).'<br />';

echo "<br/><br/><button class =\"btn btn-primary\"type=\"button\" onclick=\"location.href='./phpdownload/downloadkeyword.php?id=$timenamefolder'\"> 下載結果</button>".'<br />';
echo "<br/><font color=\"#FF0000\">csv檔為big5編碼，請使用big5編碼開啟檔案</font><br/>";

echo "<br/><button class =\"btn btn-primary\"type=\"button\" onclick=\"location.href='./tf-idfagain.php?timenamefolder=$timenamefolder'\"> 重作TF-IDF</button>";

    

?>
