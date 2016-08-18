/**
 * Created by Tab on 2016/7/12.
 */

$(function () {
    init();
});

function init() {
    usernameFlag = false;  
    passwordFlag = false;  
    checknumFlag = false; 
    usernameBindBlur();
    passwdBindBlur();
    checknumBindBlur();
    loginBindClick();
}

function usernameBindBlur() {
    $("#username").children("input").blur(function () {
        var current_var = $(this).val();
        var info = $("#info-name");
        //下面开始判断用户的输入是否合法
        if(current_var.length<4||current_var.length>20){
            info.removeClass('hidden').text('用户名的长度范围为4-20');
        }else {
             if(current_var.search(/[\s$%&*^~]/) != -1){
                info.removeClass('hidden').text('您输入的用户名有特殊字符');
             }else {
                 info.addClass('hidden');
                 usernameFlag = true;
             }
        }
    });

}

function passwdBindBlur() {
    $("#passwd").children("input").blur(function () {
        var current_var = $(this).val();
        var info = $("#info-passwd");

        //下面开始判断用户的输入是否合法
        if(current_var.length<6||current_var.length>20){
            info.removeClass('hidden').text('密码的长度范围为6-20');
        }else {
             if(current_var.search(/\s/) != -1){
                info.removeClass('hidden').text('您输入的用密码含有有空格');
             }else {
                 info.addClass('hidden');
                 passwordFlag = true
             }
        }
    });

}

function checknumBindBlur() {
    $("#checknum").children("input").blur(function () {
        checknumFlag = true;
    });

}

function myTrigger() {
    $("#username").children("input").trigger('blur');
    $("#passwd").children("input").trigger('blur');
    $("#checknum").children("input").trigger('blur');
}

function loginBindClick() {
    $(".login button").click(function () {
        myTrigger();
        var ret = false;
        if(usernameFlag  & passwordFlag & checknumFlag){
            ret = true;
        }else {
            alert('您的输入有误，请重新登陆');
        }
        return ret;
    });
}



