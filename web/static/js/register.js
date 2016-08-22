/**
 * Created by Tab on 2016/7/12.
 */

$(function () {
    init();
});

function init() {
    usernameFlag = false;
    emailFlag = false;
    passwordFlag = false;
    checkpsdFlag = false;
    checknumFlag = false;
    passwd = '';  // 保存用户输入的密码
    usernameBindBlur();
    emailBindBlur();
    passwdBindBlur();
    checkpsdBindBlur();
    checknumBindBlur();
    registerBindClick();
}

function usernameBindBlur() {
    $("#username").children("input").blur(function () {
        var current_var = $(this).val();
        console.log(current_var);
        var info = $("#info-name");

        if (current_var.length < 4 || current_var.length > 20) {
            info.removeClass('hidden').text('用户名的长度范围为4-20');
        } else {
            if (current_var.search(/[\s$%&*^~]/) != -1) {
                info.removeClass('hidden').text('您输入的用户名有特殊字符');
            } else {
                $.ajax({
                    type:'POST',
                    url: '/check_username',
                    data: {'username': current_var},
                    success: function (callback) {
                        if (callback == 'true') {
                            //下面开始判断用户的输入是否合法
                            info.removeClass('hidden').text('用户名已存在');
                        } else {
                            info.addClass('hidden');
                            usernameFlag = true;
                        }
                    }
                });
            }

            // 发ajax请求验证数据库里面用户名是否存在
            // $.post({
            //     url: '/check_username',
            //     data: {'username': current_var},
            //     success: function (callback) {
            //         if (callback == 'true') {
            //             //下面开始判断用户的输入是否合法
            //             if (current_var.length < 4 || current_var.length > 20) {
            //                 info.removeClass('hiden').text('用户名的长度范围为4-20');
            //             } else {
            //                 if (current_var.search(/[\s$%&*^~]/) != -1) {
            //                     info.removeClass('hiden').text('您输入的用户名有特殊字符');
            //                 } else {
            //                     info.addClass('hiden');
            //                     usernameFlag = true;
            //                 }
            //             }
            //         }
            //         else {
            //             info.removeClass('hiden').text('用户名已存在');
            //         }
            //     }
            // });
        }
    })
}

    function emailBindBlur() {
        $("#email").children("input").blur(function () {
            var current_var = $(this).val();
            var info = $("#info-email");

            var email_check = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
            console.log(55);
            if (email_check.test(current_var)) {
                info.addClass('hidden');
                emailFlag = true;
            } else {
                info.removeClass('hidden').text('您输入的邮箱格式不对')
            }
        });
    }

    function passwdBindBlur() {
        $("#passwd").children("input").blur(function () {
            var current_var = $(this).val();
            var info = $("#info-passwd");

            //下面开始判断用户的输入是否合法
            if (current_var.length < 6 || current_var.length > 20) {
                info.removeClass('hidden').text('密码的长度范围为6-20');
            } else {
                if (current_var.search(/\s/) != -1) {
                    info.removeClass('hidden').text('您输入的用密码含有有空格');
                } else {
                    info.addClass('hidden');
                    passwordFlag = true
                }
                passwd = current_var;
            }
        });
    }

    function checkpsdBindBlur() {
        $("#checkpsd").children("input").blur(function () {
            var current_var = $(this).val();
            var info = $("#info-checkpsd");
            //下面开始判断用户的输入是否合法
            if (current_var != passwd) {
                info.removeClass('hidden').text('两次输入的密码不一致');
            } else {
                info.addClass('hidden');
                checkpsdFlag = true;
            }
        });
    }

// 邮箱验证码
    function checknumBindBlur() {
        checknumFlag = true;
    }

    function registerBindClick() {
        $(".register button").click(function () {
            var ret = false;
            myTrigger();
            if (usernameFlag & emailFlag & passwordFlag & checkpsdFlag & checknumFlag) {
                console.log(111)
                ret = true;
            } else {
                alert('您的输入有误，请重新输入');
            }
            return ret;
        });
    }

    function myTrigger() {
        $("#username").children("input").trigger('blur');
        $("#passwd").children("input").trigger('blur');
        $("#checknum").children("input").trigger('blur');
        $("#email").children("input").trigger('blur');
        $("#checkpsd").children("input").trigger('blur')
    }
