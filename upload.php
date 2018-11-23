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
    if (file_exists($uploaddir. $file_name)){
      echo '檔案已覆蓋。<br/>';
      unlink($uploaddir. $file_name);
    } 
    $file = $_FILES[$file_id]['tmp_name'];
    $dest = $uploaddir . $file_name;
    # 將檔案移至指定位置
    move_uploaded_file($file, $dest);
    
  } else {
   echo '錯誤代碼：' . $_FILES[$file_id]['error'] . '未上傳檔案或字典<br/>';

  }
}



//$timenamefolder = GetIP();#製作多個使用者時的分辨用資料夾，以時間與亂數0~100為命名規則
//if(!$timenamefolder){
$timenamefolder=date("YmdHis").rand(0,100);
//}
if( $_POST["excel_content"]){
  $excel_content = $_POST["excel_content"];#
}else{
  $excel_content = "no-excel";
}
if($_POST["excel_category"]){
  $excel_category = $_POST["excel_category"];#
}else{
  $excel_category = "no-excel";
}



uploadfile('add_file','./all_dict/'.$timenamefolder.'/','new_dict.txt');
uploadfile('del_file','./all_dict/'.$timenamefolder.'/','all_stop.txt');

include("./phpadddict/add_new.php");
echo Do_new($timenamefolder,$_POST["new_word"]);

include("./phpadddict/add_del.php");
echo Do_del($timenamefolder,$_POST["del_word"]);

$time1=date("Y-m-d H:i:s");#上傳開始時間

$uploadhtm = 'index.html';
$uploaddir = './data/'.$timenamefolder.'/';//儲存路徑


$f_name = explode(".",$_FILES['my_file']['name']);

uploadfile('my_file',$uploaddir,"data.".end($f_name));


$time2 = date("Y-m-d H:i:s");
/*if (!file_exists('./export/'.$timenamefolder)){
  mkdir('./export/'.$timenamefolder);
}*/
// $output=shell_exec("/usr/local/bin/python3 tokens.py $timenamefolder $filename");#macOS呼叫與傳值給python



//echo $excel_category;
//echo $excel_content;
$data = "{
    \"excel_category\":\"$excel_category\",
    \"excel_content\":\"$excel_content\"
}";
file_put_contents( './excel_category.json' , $data);

$cmd = 'python ./pyprogram/jieba-mutliprocessing.py '.$timenamefolder;//.' '.'  2>error.txt 2>&1';

echo shell_exec($cmd);#Windows系統呼叫與傳值給python


if($_POST["tfidf"] == '1')
{
  echo exec("python ./pyprogram/tf-idftry.py ".$timenamefolder." ".$_POST["tfidf_rank"],$array, $ret);
}

else{
  echo $_POST["tfidf"]."沒有跑tf-idf<br/>";
}

$time3 = date("Y-m-d H:i:s");
echo '開始時間'.$time1.'<br />';
echo '上傳時間統計：'.exec_time($time2,$time1).'<br />';
echo '分詞時間統計：'.exec_time($time3,$time2).'<br />';
echo '總執行時間：'.exec_time($time3,$time1).'<br />';
echo '<br />'."<button class =\"btn btn-primary\" type=\"button\" onclick=\"location.href='./phpdownload/downloadcut.php?id=".$timenamefolder."'\">下載斷詞</button>".'<br />'.'<br />';
        

if($_POST["tfidf"] == '1'){   
    echo "<button class =\"btn btn-primary\"type=\"button\" onclick=\"location.href='./phpdownload/downloadTF-IDF.php?id=$timenamefolder'\"> 下載TF-IDF</button>".'<br />'.'<br />';

    echo "<button class =\"btn btn-primary\"type=\"button\" onclick=\"location.href='./phpdownload/downloadkeyword.php?id=$timenamefolder'\"> 下載keyword</button>".'<br />';
    echo "<br/><font color=\"#FF0000\">csv檔為utf-8編碼，請使用utf-8編碼開啟檔案</font><br/>";
    echo "<br/><button class =\"btn btn-primary\"type=\"button\" onclick=\"location.href='./tf-idfagain.html'\"> 重作TF-IDF</button>".'<br />';
    echo "<br/><font color=\"#FF0000\">如要重做，請複製以下數字</font><p>".$timenamefolder."</p>";
}
  
echo exec("python ./pyprogram/del_file.py ".$timenamefolder,$array1, $ret1);
    

?>
