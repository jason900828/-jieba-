<?php


function Do_del($Client_IP_d,$txt_d){
  if (!file_exists("./all_dict_user/")){
    mkdir("./all_dict_user/");
  }
  if (!file_exists("./all_dict_user/".$Client_IP_d."/")){
    mkdir("./all_dict_user/".$Client_IP_d."/");
  }
  
  //$txt = $_GET["del_word"];
  $myfile = fopen("./all_dict/user_stop.txt", "r")or die("Unable to open file!");
  $str = '';
  while(! feof($myfile)){
    $str =  $str.fgets($myfile)."\n";
  }
  $user_a = mb_split("\n",$str);
  fclose($myfile);
  $myfile = fopen("./all_dict/user_stop.txt", "a")or die("Unable to open file!");
  $txt_d = mb_convert_encoding($txt_d, 'utf-8');
  $txt_a =  mb_split("\n",$txt_d);

  for($i=0;$i<count($txt_a);$i++){
    if(in_array($txt_a[$i],$user_a)){
        continue;
    }
    else if($txt_a[$i] == "你可以選擇在這打上需要的詞彙："){
        continue;
    }
    else{
      fwrite($myfile, $txt_a[$i]."\n");
    }
  }
  fclose($myfile);
  echo shell_exec("python ./pyprogram/stopword.py $Client_IP_d");


}




?>
