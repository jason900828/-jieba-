function getFileExtension(filename) 
{
  return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
  //http://www.jstips.co/zh_tw/javascript/get-file-extension/
}
function delChange()
{
   var fullPath_d = document.getElementById('del_file').value;//get 檔案路徑
  
  if (fullPath_d) 
  {
    var startIndex = (fullPath_d.indexOf('\\') >= 0 ? fullPath_d.lastIndexOf('\\') : fullPath_d.lastIndexOf('/'));
    /*indexOf() 方法可返回某個指定的字符串值在字符串中首次出現的位置。
    lastIndexOf() 方法可返回一個指定的字符串值最後出現的位置，在一個字符串中的指定位置從後向前搜索
    條件 ? 值一 : 值二   當條件==true時，返回值一，false時，返回值二。    但是如果條件==true，值一卻==false(ex:null,0...)時，將返回值二*/
    var filename_d = fullPath_d.substring(startIndex);
    //傳回 String 物件中指定之位置的子字串，substring(start [, end])，如果省略 end，便會傳回從 start 一直到原始字串結尾的字元。

    if (filename_d.indexOf('\\') === 0 || filename_d.indexOf('/') === 0)
    {// ===  equal value and equal type
      filename_d = filename_d.substring(1);
    }
    var F_Extension_d = getFileExtension(filename_d);
    var label=document.getElementById("file_label2");
    if(F_Extension_d!='txt')
    {
       alert('上傳錯誤!!');
       document.getElementById('del_file').value = '';
       label.innerText='或是上傳字典檔(txt)';
    }
    else
    {
      label.innerText=filename_d;
    }
  }
}
function delclick()
{
  var label=document.getElementById("del_word");
      label.innerText='';
}