$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();


});

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_test_minders').bootstrapTable({
            url: '/get_minders.json',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100, 500],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: 'id'
            },  {
                field: 'name',
                title: '名称'
            },{
                field: 'module',
                title: '模块'
            },{
                field: 'description',
                title: '说明'
            },
             {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_minder?id='+ row.id + '\')">编辑信息</a> ';
                        var d = '<a href="javascript:;" onclick="window.location.href=(\'/view_minder_json?id='+ row.id + '\')">查看内容</a> ';
                        var e = '<a href="javascript:;" onclick="window.location.href=(\'/edit_minder_json?id='+ row.id + '\')">编辑内容</a> ';
                        var b = '<a href="javascript:;" onclick="copy_minder_save(\'' + row.id + '\')">复制</a> ';
                        var c = '<a href="javascript:;" onclick="delete_test_minder(\'' + row.id + '\')">删除</a> ';
                        return a+e+d+b+c;
                        }
                }
                ]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            name: $("#name").val()
        };
        return temp;
    };
    return oTableInit;
};

function searchMinders(){
    var name=$('#name').val();
   $('#tb_test_minders').bootstrapTable('refresh', {url: '/get_minders.json',query:{'name': name}});
}

 // 编辑表单
function get_edit_minder_info(active_id)
  {
//    alert(active_id)
    if(!active_id)
    {
      alert('Error！');
      return false;
    }
    // var form_data = new Array();

    $.ajax(
        {
          url: "/get_minders.json",
          data:{"id":active_id,"type":"edit"},
          type: "get",
          dataType:"json",
          beforeSend:function()
          {
            // $("#tip").html("<span style='color:blue'>正在处理...</span>");
            return true;
          },
          success:function(data)
          {
            console.log(data);
            console.log(data.code);
            console.log(data.minder);
            console.log(data.code==200);
            if(data.code == 200)
            {
              console.log('start');
              // 解析json数据
              var data = data;
              var data_obj = data.minder;
              console.log(data_obj.id);
              console.log(data_obj.name);
              console.log(data_obj.module);
              console.log(data_obj.description);

              // 赋值
              $("#id").val(data_obj.id);
              $("#name").val(data_obj.name);
              $("#module").val(data_obj.module);
              $("#description").val(data_obj.description);
            }

            else
            {
              $("#tip").html("<span style='color:red'>失败，请重试</span>");
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

    return false;
  }


// submit form
function submitAddMinderForm() {
//   $("#new_test_minder").validate();
      $.ajax(
    {
        url: "/save_new_test_minder.json",
        data:{"type":"add","name":$("#name").val(),"module":$("#module").val(),"description":$("#description").val()},
        type: "post",
        dataType:"json",
        beforeSend:function()
        {
        return true;
        },
        success:function(data)
        {
        console.log(data);
        if(data)
        {
            // 解析json数据
            var data = data;
            if(data.code==200){
            alert('success!');
            window.location.href=('/test_minders');
            // alert
            }else{
            alert('code is :'+data.code+' and message is :'+data.msg);
            }
        }

        else
        {
            // $("#tip").html("<span style='color:red'>失败，请重试</span>");
        console.log(data);
        window.location.href=('/test_minders');
        }
        },
        error:function()
        {
        console.log(data);
        window.location.href=('/test_minders');
        },
        complete:function()
        {
        // $('#tips').hide();
        window.location.href=('/test_minders');
        }
});
   }

// submit form
function submitEditForm() {
//   $("#edit_test_minder").validate();
      $.ajax(
    {
        url: "/save_new_test_minder.json",
        data:{"id":$("#id").val(),"type":"update","name":$("#name").val(),"module":$("#module").val(),"description":$("#description").val()},
        type: "post",
        dataType:"json",
        beforeSend:function()
        {
        return true;
        },
        success:function(data)
        {
        console.log(data);
        if(data)
        {
            // 解析json数据
            var data = data;
            if(data.code==200){
            alert('success!');
            window.location.href=('/test_minders');
            // alert
            }else{
            alert('code is :'+data.code+' and message is :'+data.msg);
            }
        }

        else
        {
            // $("#tip").html("<span style='color:red'>失败，请重试</span>");
        window.location.href=('/test_minders');
        console.log(data);
        }
        },
        error:function()
        {
        console.log(data);
        window.location.href=('/test_minders');
        },
        complete:function()
        {
        // $('#tips').hide();
        window.location.href=('/test_minders');
        }
});
   }



function copy_minder(){
    var minder_id = document.getElementById('minderId').value;
//    alert(minder_id);
    if (minder_id != ""){
        copy_minder_save(minder_id);

    }else{
        alert('id is null!');
    }

}

function copy_minder_save(minder_id){
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
            window.location.href=('/edit_minder?id='+data.id);
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


function delete_test_minder(minder_id){
        $.ajax(
    {
        url: "/delete_test_minder.json",
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
            window.location.href=('/test_minders');
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
