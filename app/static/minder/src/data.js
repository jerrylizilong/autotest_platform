
function exportData(){
    var jsonData=editor.minder.exportJson();
    jsonData = JSON.stringify(jsonData);
    console.log(jsonData);
    var minder_id = document.getElementById('minderId').value;
    $.ajax(
    {
        url: "/save_test_minder_content.json",
        data:{"content":jsonData,"id":minder_id},
        type: "post",
        dataType:"json",
        beforeSend:function()
        {
        return true;
        },
        success:function(data)
        {
        if(data)
        {
            // 解析json数据
            var data = data;
            if(data.code==200){
            alert('success!');
            // alert
            }else{
            alert('code is :'+data.code+' and message is :'+data.msg);
            }
        }

        else
        {
            // $("#tip").html("<span style='color:red'>失败，请重试</span>");
        alert('操作失败');
        }
        },
        error:function()
        {
        alert('请求出错');
        },
        complete:function()
        {
        // $('#tips').hide();
        }
});

}


function init(minder_id,refreshJson){
//    localStorage.removeItem('__dev_minder_content');
    document.getElementById('minderId').value = minder_id;
    if (minder_id != ""){

        $.ajax(
    {
        url: "/get_minders.json",
        data:{"id":minder_id},
        type: "get",
        dataType:"json",
        beforeSend:function()
        {
        return true;
        },
        success:function(data)
        {
        if(data)
        {
            // 解析json数据
            var data = data;
            if(data.code==200){
//            alert('success!');
            console.log(JSON.parse(data.content));
//            editor.minder.importJson(JSON.parse(data.content));
            if (data.content!='{}'){
                if (refreshJson==1){
                editor.minder.importJson(JSON.parse(data.content));
                alert('刷新成功！');
                }else {
                    window.localStorage.__dev_minder_content=data.content;
                    }
            }else{
                localStorage.removeItem('__dev_minder_content');
                if (refreshJson==1){
                   alert('刷新成功！');
                }
            }
            // document.location.reload();
            // alert
            }else{
            alert('code is :'+data.code+' and message is :'+data.msg);
            }
        }

        else
        {
            // $("#tip").html("<span style='color:red'>失败，请重试</span>");
        alert('操作失败');
        }
        },
        error:function()
        {
        alert('请求出错');
        },
        complete:function()
        {
        // $('#tips').hide();
        }
});
    }else{
        alert('id is null!');
    }

}




function copy_minder(){

    var minder_id = document.getElementById('minderId').value;
//    alert(minder_id);
    if (minder_id != ""){

        $.ajax(
    {
        url: "/copy_test_minder.json",
        data:{"id":minder_id},
        type: "post",
        dataType:"json",
        beforeSend:function()
        {
        return true;
        },
        success:function(data)
        {
        if(data)
        {
            // 解析json数据
            var data = data;
            if(data.code==200){
            alert('success!');
            window.location.href=('/edit_minder_json?id='+data.id);
            // document.location.reload();
            // alert
            }else{
            alert('code is :'+data.code+' and message is :'+data.msg);
            }
        }

        else
        {
            // $("#tip").html("<span style='color:red'>失败，请重试</span>");
        alert('操作失败');
        }
        },
        error:function()
        {
        alert('请求出错');
        },
        complete:function()
        {
        // $('#tips').hide();
        }
});
    }else{
        alert('id is null!');
    }

}

