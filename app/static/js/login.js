$(document).ready(function(){
    // 初始化popover
    $("[data-toggle='popover']").popover();
    // 关联 眼睛 事件
    $("#eye").mousedown(open);
    $("#eye2").mousedown(open);
    $("#eye3").mousedown(open);
    $("#eye").mouseup(close);
    $("#eye2").mouseup(close);
    $("#eye3").mouseup(close);
    // 点击输入框后清空警告和popover
    $("#user").focus(inputFocus);
    $("#pwd").focus(inputFocus);
    $("#newPwd").focus(inputFocus);
    $("#newPwdR").focus(inputFocus);
    // 提交判断
    toastr.options["positionClass"] = "toast-top-center";
    toastr.options["timeOut"] = "5000";
    $("#submit").click(function(){
        if($("#user").val() == ""){inputError("#user");return false;}
        if($("#pwd").val() == ""){inputError("#pwd");return false;}
        if($("#newPwd").val() == ""){inputError("#newPwd");return false;}
        if($("#newPwdR").val() == ""){inputError("#newPwdR");return false;}
        if($("#newPwd").val() != $("#newPwdR").val()){
            toastr.error("两次输入密码不一致！");inputError("#newPwd");inputError("#newPwdR");
            return false;
        }
        var regex = new RegExp('(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,30}');
        var regex2 = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,30}');
        var regex3 = new RegExp('(?=.*[0-9])(?=.*[a-z])(?=.*[^a-zA-Z0-9]).{8,30}');
        var regex4 = new RegExp('(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,30}');
        data = $("#newPwd").val()
        if(!(regex.test(data) || regex2.test(data) || regex3.test(data) || regex4.test(data))){
            toastr.error("新密码不符合复杂度要求！");inputError("#newPwd");inputError("#newPwdR");
            return false;
        }

        // 提交post请求
         $.ajax({
			    type: 'POST',
			    url: document.URL,
			    data: $("form").serialize(),
			    dataType: "json",
			    success: detect_result,
			    failed: function(){toastr.error("提交请求失败, 服务器或者网络故障！")},
			    error: function(){toastr.error("提交请求失败, 服务器或者网络故障！")}
		    });
        return false;
    });
});
function open(){
    var id = $(this).attr('id');
    var input = '';
    if(id == 'eye'){input = '#pwd';}
    else if(id == 'eye2'){input = '#newPwd';}
    else if(id == 'eye3'){input = '#newPwdR';}
    $(input).attr('type', 'text');
    $(this).removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
};
function close(){
    var id = $(this).attr('id');
    var input = '';
    if(id == 'eye'){input = '#pwd';}
    else if(id == 'eye2'){input = '#newPwd';}
    else if(id == 'eye3'){input = '#newPwdR';}
    $(input).attr('type', 'password');
    $(this).removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
}
function inputFocus(){
    $(this).popover('hide');
    $(this).parent().removeClass('has-error');
}
function inputError(id){
    $(id).popover('show');
    $(id).parent().addClass('has-error');
}
function detect_result(data){
    if(data["success"])
    {
        toastr.success("密码修改成功!");
        $("#user").val("");
        $("#pwd").val("");
        $("#newPwd").val("");
        $("#newPwdR").val("");
    }
    else
    {
        toastr.error(data["result"]);
    }

}