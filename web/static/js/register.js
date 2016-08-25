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
    // checknumFlag = false;
    passwd = '';  // 保存用户输入的密码
    usernameBindBlur();
    emailBindBlur();
    passwdBindBlur();
    checkpsdBindBlur();
    // checknumBindBlur();
    registerBindClick();
    
    BindSendMsg()
}

// 前端验证用户名，并且发送ajax验证用户名是否已经存在
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
                    type: 'POST',
                    url: '/check_username',
                    data: {'username': current_var},
                    success: function (callback) {
                        if (callback == 'True') {
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

// 前端验证邮箱，并且发送ajax验证邮箱是否已经注册过
function emailBindBlur() {
    $("#email").children("input").blur(function () {
        var current_var = $(this).val();
        var info = $("#info-email");

        var email_check = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
        if (email_check.test(current_var)) {
            $.ajax({
                    type: 'POST',
                    url: '/check_email',
                    data: {'email': current_var},
                    success: function (callback) {
                        if (callback == 'True') {
                            //下面开始判断用户的输入是否合法
                            info.removeClass('hidden').text('该邮箱已存在');
                        } else {
                            info.addClass('hidden');
                            emailFlag = true;
                        }
                    }
                });
            // info.addClass('hidden');
            // emailFlag = true;
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
// function checknumBindBlur() {
//     checknumFlag = true;
// }

// function registerBindClick() {
//     $(".register button").click(function () {
//         var ret = false;
//         myTrigger();
//         if (usernameFlag & emailFlag & passwordFlag & checkpsdFlag ) {
//             console.log(111)
//             ret = true;
//         } else {
//             alert('您的输入有误，请重新输入');
//         }
//         return ret;
//     });
// }


function registerBindClick() {
    $(".register button").click(function () {
        var ret = false;
        myTrigger();
        if (usernameFlag & emailFlag & passwordFlag & checkpsdFlag) {
            var register_info = {};
            $(".register-content form input").each(function () {
                var name = $(this).attr('name');
                var value = $(this).val();
                register_info[name] = value
            });
            $.ajax({
                url:'/register',
                type:'POST',
                data: register_info,
                dataType:'json',
                success:function (arg) {
                    if (arg.status){
                        window.location.href = '/index';
                    }else {
                        $.each(arg.message, function(k,v){
                            $('.register-content form input[name="'+ k +'"]').parent().next().removeClass('hidden').text(v);
                        })
                    }
                }
            })
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



// 像注册的Email邮箱发送邮箱验证码
function BindSendMsg() {
    $("#fetch-code").click(function () {
        var email = $("#email").children("input").val();
        console.log(email);
        if (!emailFlag) {
            // $('#register_error_summary').text('请输入注册邮箱');
            $("#info-email").removeClass('hidden').text('请输入正确的邮箱');
            return;
        }
        if ($(this).hasClass('sending')) {
            return;
        }
        var ths = $(this);
        var time = 60;

        $.ajax({
            url: "/send_msg",
            type: 'POST',
            data: {email: email},
            // dataType: 'json',
            success: function (arg) {
                if (arg=='True') {
                    ths.addClass('sending');
                    var interval = setInterval(function () {
                        ths.text("已发送(" + time + ")");
                        time -= 1;
                        if (time <= 0) {
                            clearInterval(interval);
                            ths.removeClass('sending');
                            ths.text("获取验证码");
                        }
                    }, 1000);
                    
                } else {
                    $("#info-checkcode").removeClass('hidden').text(arg);
                }
            }
        });

    });
}