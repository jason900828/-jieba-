<?php

$myfile = fopen("../all_dict/del_words.txt", "w")or die("Unable to open file!");
$txt = $_GET["del_word"];
$txt = mb_convert_encoding($txt, 'utf-8');
fwrite($myfile, $txt);
fclose($myfile);

echo shell_exec("python ../pyprogram/stopword.py ");

header("location: ../index.html");
?>