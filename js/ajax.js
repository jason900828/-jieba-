$(document).ready(function (e){
    $("#loader").hide();
    $("#loader2").hide();
    $(document).ajaxStart(function(){
        $("#loader").show();
        $("#loader2").show();
        $("#Description").hide();
        $("#bar1").hide();
        $("#bar2").hide();
        $("#bar3").hide();
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
                d = data;
                $("#result").html(d);
                $("#loader").hide();
                $("#loader2").hide();
            },
            
            error: function(){}             
        });
    }));
    $(document).ajaxStop(function(){

        
    });
    
});



