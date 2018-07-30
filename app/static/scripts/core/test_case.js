
// submit form
function submitAddForm() {
   $("#new_test_case").validate();
   $.validator.setDefaults({
        submitHandler: function() {
            document.getElementById("new_test_case").submit();
    }
});
   }


$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();


});

function get_test_case_detail(id){
  $.ajax({
  url: '/test_case.json',
  method: 'get',
  data: {'id':id},
  success: success,
  dataType: dataType
});
}

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_test_cases').bootstrapTable({
            url: '/test_case.json',         //请求后台的URL（*）
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
            }, {
                field: 'module',
                title: '模块'
            }, {
                field: 'name',
                title: '名称'
            }, {
                field: 'steps',
                title: '步骤'
            }, {
                field: 'description',
                title: '描述'
            },
             {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_test_case?id='+ row.id + '\')">编辑</a> ';
                        var b = '<a href="javascript:;" onclick="copy_test_case(\'' + row.id + '\')">复制</a> ';
                        var c = '<a href="javascript:;" onclick="run_test_case(\'' + row.id + '\')">执行</a> ';
                        var d = '<a href="javascript:;" onclick="window.location.href=(\'/test_case_runhistory?id='+ row.id + '\')">执行结果</a> ';
                        var e = '<a href="javascript:;" onclick="delete_test_case(\'' + row.id + '\')">删除</a> ';
                        return a+b+c+d+e;
                        }
                }
                ]
        });
    };

function edit(index) {
    window.location.href=('/edit_test_case?id='+index);
}

function operateFormatter(value, row, index) {
            return [
                '<button type="button" class="RoleOfEdit btn btn-default  btn-sm" style="margin-right:15px;">编辑</button>',
                '<button type="button" class="RoleOfDelete btn btn-default  btn-sm" style="margin-right:15px;">删除</button>'
            ].join('');
        }

window.operateEvents = {
            'click .RoleOfEdit': function (e, value, row, index) {
                window.location.href=('/add_test_case');
         },
            'click .RoleOfDelete': function (e, value, row, index) {
                alert("B");
         }
         }


    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            name: $("#name").val(),
            module: $("#selectModule").val(),
            type:"test_cases"
        };
        return temp;
    };
    return oTableInit;
};


function searchTestCase(test_case_id){
//    alert(1)
    var $tb_departments = $('#tb_test_cases');
    $tb_departments.bootstrapTable('refresh', {url: '/test_case.json',data:{id: test_case_id,type:"test_case"}});
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
          url: "/test_case.json",
          data:{"id":active_id,"type":"test_case"},
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
//              var data_obj0 = eval("("+data+")");
//              var data_obj = eval("("+data_obj0+")");
              var data_obj = data.rows

              // 赋值
              $("#id").val(active_id);
              $("#name").val(data_obj.name);
              $("#steps").val(data_obj.steps);
              $("#description").val(data_obj.description);
              $("#type").val(data_obj.isPublic);
              var isPublic = data_obj.isPublic;
              if(isPublic == 1)
              {
                $("#type").val('公共用例');
                setModule('公共用例');
              }else{
                $("#type").val('普通用例');
                setModule('普通用例');
              }
              $("#module").val(data_obj.module);
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



// 删除表单
function delete_test_case(active_id)
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
            url: "delete_test_case",
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

 function run_test_case(test_case_id){
         $.ajax(
        {
          url: "/runtest.json",
          data:{"id":test_case_id,"type":"test_case"},
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
              alert('success!');
              window.location.href=('/test_case_runhistory?id='+ test_case_id  )
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

 function copy_test_case(test_case_id){
         $.ajax(
        {
          url: "/copy_test_case",
          data:{"id":test_case_id},
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