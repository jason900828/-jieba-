$(document).ready(function (e){
    $("#loader").hide();
    $("#loader2").hide();
    $(document).ajaxStart(function(){
        $("#loader").show();
        $("#loader2").show();
        $(".input").hide();
    });
    
    var d ;
    $("#uploadform").on('submit',(function(e){
        e.preventDefault();
        $.ajax({
            url: "upload.php",
            type: "POST",
            data:  new FormData(this),
            contentType: false,
            cache: false,
            processData:false,
            success: function(data){
                alert("成功執行");
                d = data;
            },
            
            error: function(){}             
        });
    }));
    $(document).ajaxStop(function(){

        $("#result").html(d);
        $("#loader").hide();
        $("#loader2").hide();
    });
    
});



