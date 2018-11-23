<?php



function Do_new($Client_IP_n,$txt_n){
  if (!file_exists("./all_dict/".$Client_IP_n."/")){
    mkdir("./all_dict/".$Client_IP_n."/");
  }
  $myfile = fopen("./all_dict/user_news.txt", "r")or die("Unable to open file!");
 while(! feof($myfile)){
    $str =  $str.fgets($myfile)."\n";
  }
  $user_a = mb_split("\n",$str);
  fclose($myfile);
  $myfile = fopen("./all_dict/user_news.txt", "a")or die("Unable to open file!");
  //$txt = $_GET["new_word"];
  $txt_n = mb_convert_encoding($txt_n,'utf-8');

  $txt_a =  mb_split("\n",$txt_n);

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
  echo shell_exec("python ./pyprogram/add_news.py $Client_IP_n");
}
  



?>