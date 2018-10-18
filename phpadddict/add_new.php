<?php

$myfile = fopen("../all_dict/new_words.txt", "w")or die("Unable to open file!");
$txt = $_GET["new_word"];
$txt = mb_convert_encoding($txt,'utf-8');
fwrite($myfile, $txt);
fclose($myfile);

echo shell_exec("python ../pyprogram/add_news.py ");
header("location: ../index.html");
?>