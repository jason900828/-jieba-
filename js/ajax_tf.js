$(document).ready(function (e){
    $("#loader").hide();
    $("#loader2").hide();
    $(document).ajaxStart(function(){
        $("#loader").show();
        $("#loader2").show();
        $("#Description").hide();
        $("#bar1").hide();
    });
    
    var d ;
    $("#calltf-idf").on('submit',(function(e){
        e.preventDefault();
        $.ajax({
            url: "calltf-idf.php",
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



