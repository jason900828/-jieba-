
var filename ;
var F_Extension;
var tfidf_r;


function boxChange(){

  if(document.getElementById("tfidf").checked == true)
  {
    if(filename == null)
    {
      alert('尚未上傳檔案');
      document.getElementById("tfidf").checked = false;
    }
    F_Extension = getFileExtension(filename);

    if ((F_Extension!='zip')&&(F_Extension!='xlsx'))
    {
      alert("請上傳zip或xlsx檔才可開啟tf-idf");
      document.getElementById("tfidf").checked = false;
      tfidf_r = document.getElementById('tfidf_r');
      tfidf_r.style.visibility = "hidden";
    }
    else
    {
      tfidf_r = document.getElementById('tfidf_r');
      tfidf_r.style.visibility = "visible";
    }
    
  }
  else
  {
      tfidf_r = document.getElementById('tfidf_r');
      tfidf_r.style.visibility = "hidden";
  }

}
function getFileExtension(filename) 
{
  return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
  //http://www.jstips.co/zh_tw/javascript/get-file-extension/
}
function uploadChange()
{

  var fullPath = document.getElementById('my_file').value;//get 檔案路徑
  var excel = document.getElementById('excel');
  if (fullPath) 
  {
    var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
    /*indexOf() 方法可返回某個指定的字符串值在字符串中首次出現的位置。
    lastIndexOf() 方法可返回一個指定的字符串值最後出現的位置，在一個字符串中的指定位置從後向前搜索
    條件 ? 值一 : 值二   當條件==true時，返回值一，false時，返回值二。    但是如果條件==true，值一卻==false(ex:null,0...)時，將返回值二*/
    filename = fullPath.substring(startIndex);
    //傳回 String 物件中指定之位置的子字串，substring(start [, end])，如果省略 end，便會傳回從 start 一直到原始字串結尾的字元。

    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) 
    {// ===  equal value and equal type
      filename = filename.substring(1);
    }
    F_Extension = getFileExtension(filename);
    if((F_Extension!='zip')&&(F_Extension!='xlsx'))
    {
      document.getElementById("tfidf").checked = false;
      tfidf_r = document.getElementById('tfidf_r');
      tfidf_r.style.visibility = "hidden";
    }
    
    var label=document.getElementById("file_label");
    label.innerText=filename;

    if((F_Extension!='zip')&&(F_Extension!='txt')&&(F_Extension!='xlsx'))
    {
      alert('上傳錯誤!!');
      document.getElementById('my_file').value = '';
      label.innerText='點擊上傳';//虽然file的value不能设为有字符的值，但是可以设置为空值

    }
    
    if(F_Extension=='xlsx')
    {
      excel.style.display = ""; // 显示元素
      
    }
    else
    {
      excel.style.display = "none";
      
    }
  }
}
function addChange()
{
   var fullPath_a = document.getElementById('add_file').value;//get 檔案路徑
  
  if (fullPath_a) 
  {
    var startIndex = (fullPath_a.indexOf('\\') >= 0 ? fullPath_a.lastIndexOf('\\') : fullPath_a.lastIndexOf('/'));
    /*indexOf() 方法可返回某個指定的字符串值在字符串中首次出現的位置。
    lastIndexOf() 方法可返回一個指定的字符串值最後出現的位置，在一個字符串中的指定位置從後向前搜索
    條件 ? 值一 : 值二   當條件==true時，返回值一，false時，返回值二。    但是如果條件==true，值一卻==false(ex:null,0...)時，將返回值二*/
    var filename_a = fullPath_a.substring(startIndex);
    //傳回 String 物件中指定之位置的子字串，substring(start [, end])，如果省略 end，便會傳回從 start 一直到原始字串結尾的字元。

    if (filename_a.indexOf('\\') === 0 || filename_a.indexOf('/') === 0) 
    {// ===  equal value and equal type
      filename_a = filename_a.substring(1);
    }
    var F_Extension_a = getFileExtension(filename_a);
    var label=document.getElementById("file_label1");
    if(F_Extension_a!='txt')
    {
       alert('上傳錯誤!!');
       label.innerText='或是上傳字典檔(txt)';
       document.getElementById('add_file').value = '';
    }
    else
    {
      label.innerText=filename_a;
    }
  }
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
       document.getElementById('del_file').value = "";
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
function newclick()
{
  var label=document.getElementById("new_word");
      label.innerText='';
}