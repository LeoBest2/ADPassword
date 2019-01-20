$(document).ready(function(){
    $(".modal.fade").modal({show: true})
    $("#submit1").click(function(){
        $.post("/log/login",{pwd:$("#pwd").val()},function(result){
            location.reload();
        });
        return true;
    });
});