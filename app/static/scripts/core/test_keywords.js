

$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();


});

// submit form
function submitAddForm() {
   $("#new_test_keyword").validate();
   $.validator.setDefaults({
        submitHandler: function() {
            document.getElementById("new_test_keyword").submit();
    }
});
   }


// submit form
function submitEditForm() {
   $("#edit_test_keyword").validate();
   $.validator.setDefaults({
        submitHandler: function() {
            document.getElementById("edit_test_keyword").submit();
    }
});
   }


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_test_keywords').bootstrapTable({
            url: '/test_keywords.json',         //请求后台的URL（*）
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
                field: 'keyword',
                title: '名称'
            },{
                field: 'description',
                title: '说明'
            },{
                field: 'paraCount',
                title: '参数数量'
            }, {
                field: 'template',
                title: '模板'
            }, {
                field: 'example',
                title: '例子'
            },
             {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_test_keyword?id='+ row.id + '\')">编辑</a> ';
                        var b = '<a href="javascript:;" onclick="copy_test_keyword(\'' + row.id + '\')">复制</a> ';
                        var c = '<a href="javascript:;" onclick="delete_test_keyword(\'' + row.id + '\')">删除</a> ';
                        return a+b+c;
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
            keyword: $("#keyword").val()
        };
        return temp;
    };
    return oTableInit;
};

function searchKeywords(){
    var keyword=$('#keyword').val();
    var $tb_departments = $('#tb_test_keyword');
   $('#tb_test_keywords').bootstrapTable('refresh', {url: '/test_keywords.json',query:{'keyword': keyword}});
}

// 删除表单
function delete_test_keyword(active_id)
  {
    if(confirm("确认删除吗？"))
    {
      if(!active_id)
      {
        alert('Error！');
        return false;
      }

      $.ajax(
          {
            url: "delete_test_keyword",
            data:{"id":active_id, "act":"del"},
            type: "post",
            beforeSend:function()
            {
              $("#tip").html("<span style='color:blue'>正在处理...</span>");
              return true;
            },
            success:function(data)
            {
              if(data.code = 200)
              {
                alert('恭喜，删除成功！');
                $("#tip").html("<span style='color:blueviolet'>恭喜，删除成功！</span>");


                document.getElementById('btn_query').click();
              }
              else
              {
                $("#tip").html("<span style='color:red'>失败，请重试</span>");
                alert('失败，请重试'+data.msg);
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

    // var form_data = new Array();
    return false;
  }


function copy_test_keyword(keyword_id){
         $.ajax(
        {
          url: "/copy_test_keyword",
          data:{"id":keyword_id},
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
              document.location.reload();
              }else{
              alert('code is :'+data.code+' and message is :'+data.msg);
              }
            }

            else
            {
              $("#tip").html("<span style='color:red'>失败，请重试</span>");
             // alert('操作失败');
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


 // 编辑表单
function get_edit_info(active_id)
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
          url: "/test_keywords.json",
          data:{"id":active_id,"type":"test_keyword"},
          type: "get",
          dataType:"json",
          beforeSend:function()
          {
            // $("#tip").html("<span style='color:blue'>正在处理...</span>");
            return true;
          },
          success:function(data)
          {
            if(data)
            {
              // 解析json数据
              var data = data;
              var data_obj = data.rows[0]

              // 赋值
              $("#id").val(active_id);
              $("#name").val(data_obj.keyword);
              $("#paraCount").val(data_obj.paraCount);
              $("#description").val(data_obj.description);
              $("#template").val(data_obj.template);
              $("#example").val(data_obj.example);
            }

            else
            {
              $("#tip").html("<span style='color:red'>失败，请重试</span>");
             // alert('操作失败');
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

// add
function add_test_keyword()
  {
    {
      $.ajax(
          {
            url: "/add_test_keyword.json",
            data:{"name":$("#name").val(), "template":$("#template").val(), "description":$("#description").val(), "paraCount":$("#paraCount").val()},
            type: "post",
            beforeSend:function()
            {
              $("#tip").html("<span style='color:blue'>正在处理...</span>");
              return true;
            },
            success:function(data)
            {
              if(data.code == 200)
              {
                alert('恭喜，新增成功！');
                $("#tip").html("<span style='color:blueviolet'>恭喜，新增成功！</span>");


                window.location.href=('/testkeywords');
              }
              else
              {
                $("#tip").html("<span style='color:red'>失败，请重试</span>");
                alert('失败，请重试: '+data.msg);
              }
            },
            error:function()
            {
              alert('请求出错');
            }
          });

    }

    // var form_data = new Array();
    return false;
  }