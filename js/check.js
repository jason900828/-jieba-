
var filename ;
var F_Extension;
function boxChange(){
  if(document.getElementById("tfidf").checked == true){
    F_Extension = getFileExtension(filename);
    if (F_Extension!='zip'){
      alert("請上傳zip檔才可開啟tf-idf");
      document.getElementById("tfidf").checked = false;
    }
  }

}
function getFileExtension(filename) {
  return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
  //http://www.jstips.co/zh_tw/javascript/get-file-extension/
}
function uploadChange(){

  var fullPath = document.getElementById('my_file').value;//get 檔案路徑

  if (fullPath) {
    var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
    /*indexOf() 方法可返回某個指定的字符串值在字符串中首次出現的位置。
    lastIndexOf() 方法可返回一個指定的字符串值最後出現的位置，在一個字符串中的指定位置從後向前搜索
    條件 ? 值一 : 值二   當條件==true時，返回值一，false時，返回值二。    但是如果條件==true，值一卻==false(ex:null,0...)時，將返回值二*/
    filename = fullPath.substring(startIndex);
    //傳回 String 物件中指定之位置的子字串，substring(start [, end])，如果省略 end，便會傳回從 start 一直到原始字串結尾的字元。

    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {// ===  equal value and equal type
      filename = filename.substring(1);
    }
    F_Extension = getFileExtension(filename);
    if(F_Extension!='zip'){
      document.getElementById("tfidf").checked = false;
    }
  }
}


 
      


