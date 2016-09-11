
// 取消模态对话框
function CancelModal(container) {
    $("#do_add_form").find('input').val('');
    $('#do_add_modal').modal('hide')
}

// 提交form表单
function SubmitModal(formId) {
    var data_dict = {};
    $(formId).find('input, select').each(function () {
        var name = $(this).attr('name');
        var val = $(this).val();
        data_dict[name] = val
    });
    $.ajax({
        url: 'user_add',
        type: 'POST',
        data: data_dict,
        dataType: 'json',
        success: function (callback) {
            CancelModal();
            Refresh();
        }
    })
}

function DoDeleteUser() {
    var id_list = [];
    $("#table-body").find('input:checked').each(function () {
        var user_nid = parseInt($(this).attr('id'));
        id_list.push(user_nid);
    });
    console.log(id_list);
    $.ajax({
        url: '/user_delete',
        type: 'POST',
        data: {'id_list': JSON.stringify(id_list)},
        dataType: 'json',
        success:function(callback) {
            console.log(callback);
        }
    });
    $.Hide('#shade,#modal_delete');
    Refresh();
}

// 进入编辑模式
function SpecialOutEditFunc($td, editOption) {
    if (editOption == 'status') {
        $td.removeClass('padding-3');
        var selecting_val = $td.children().first().val();
        var selecting_text = $td.children().first().find("option[value='" + selecting_val + "']").text();
        $td.html(selecting_val);
        $td.attr('new-value', selecting_val);
    } else {
        $td.removeClass('padding-3');
        var selecting_val = $td.children().first().val();
        var selecting_text = $td.children().first().find("option[value='" + selecting_val + "']").text();
        $td.html(selecting_text);
        $td.attr('new-value', selecting_val);
    }
}

// 保存修改信息
function Save() {
    
    if ($('#edit_mode_target').hasClass('btn-warning')) {
        $.TableEditMode('#edit_mode_target', '#table-body');
    }
    var target_status = '#handle_status';
    var updateData = [];
    $('#table-body').children().each(function () {
        var rows = {};
        var id = $(this).attr('nid');
        var flag = false;

        $(this).children('td[edit-enable="true"]').each(function () {
            var origin = $(this).attr('origin');
            var newer = $(this).text();
            var name = $(this).attr('name');

            if (newer && newer.trim() && origin != newer) {
                rows[name] = newer;
                flag = true;
            }
        });
        if (flag) {
            rows['nid'] = id;
            updateData.push(rows);
        }
    });
    if (updateData.length < 1) {
        return;
    }
    console.log(updateData);
    updateData = JSON.stringify(updateData);
    $.ajax({
        url: 'update_user',
        type: 'POST',
        data: {'data': updateData},
        dataType:'json',
        success:function (callback) {
            console.log(callback);
            Refresh()
        }
    })
}


// 获取当前页码
function GetCurrentPage(pager) {
    var page = $(pager).find("li[class='active']").text();
    return page;
}
// 创建分页信息
function CreatePage(data,target){
    $(target).empty().append(data);
}

function ChangePage(page){
    $.ajax({
        url:'page',
        type:'POST',
        data:{'page':page},
        dataType:'json',
        success:function (callback) {
            $("#pager").empty().append(callback.page);
            $("#table-body").empty().append(callback.tbody);
        }
    })
}

// 刷新页面
function Refresh() {
    var currentPage = GetCurrentPage('#pager');
    ChangePage(currentPage);
}




