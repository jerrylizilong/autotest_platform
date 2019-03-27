
// submit form
//function submitAddForm() {
//   $("#new_test_suite").validate();
//   $.validator.setDefaults({
//        submitHandler: function() {
//            document.getElementById("new_test_suite").submit();
//    }
//});
//   }


$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

//    //2.初始化Button的点击事件
//    var oButtonInit = new ButtonInit();
//    oButtonInit.Init();

});

function get_test_suite_detail(id){
  $.ajax({
  url: '/test_suite.json',
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
        $('#tb_test_suites').bootstrapTable({
            url: '/test_suite.json',         //请求后台的URL（*）
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
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
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
                field: 'status',
                title: '状态'
            }, {
                field: 'run_type',
                title: '执行类型'
            }, {
                field: 'name',
                title: '名称'
            },  {
                field: 'description',
                title: '描述'
            },
             {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_test_suite?id='+ row.id + '\')">编辑</a> ';
                        var f = '<a href="javascript:;" onclick="copy_test_suite('+ row.id + ')">复制</a> ';
                        var b = '<a href="javascript:;" onclick="window.location.href=(\'/attach_test_batch?test_suite_id='+ row.id + '\')">关联用例</a> ';
                        var e = '<a href="javascript:;" onclick="window.location.href=(\'/test_batch_detail?test_suite_id='+ row.id + '\')">执行详情</a> ';
                        var c = '<a href="javascript:;" onclick="runtest('+ row.id + ')">执行</a> ';
                        var d = '<a href="javascript:;" onclick="delete_test_suite(\'' + row.id + '\')">删除</a> ';
                        return a +f+b+e+c+d ;
                        }
                }
                ]
        });
    };

function edit(index) {
    window.location.href=('/edit_test_suite?id='+index);
}

function operateFormatter(value, row, index) {
            return [
                '<button type="button" class="RoleOfEdit btn btn-default  btn-sm" style="margin-right:15px;">编辑</button>',
                '<button type="button" class="RoleOfDelete btn btn-default  btn-sm" style="margin-right:15px;">删除</button>'
            ].join('');
        }

window.operateEvents = {
            'click .RoleOfEdit': function (e, value, row, index) {
//                window.location.href=('/add_test_suite');
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
            status: $("#selectStatus").val(),
            run_type: $("#run_type").val()
        };
        return temp;
    };
    return oTableInit;
};

//
//var ButtonInit = function () {
//    var oInit = new Object();
//    var postdata = {};
//
//    oInit.Init = function () {
//        //初始化页面上面的按钮事件
//    };
//
//    return oInit;
//};

function searchTestSuite(){
    var $tb_departments = $('#tb_test_suites');
    $tb_departments.bootstrapTable('refresh', {url: '/test_suite.json'});
}

//
//function selectOnchang(obj){
////获取被选中的option标签选项
//var value = obj.options[obj.selectedIndex].value;
////alert(value);
//}


 // 编辑表单
function get_edit_info(active_id)
  {

    if(!active_id)
    {
      alert('Error！');
      return false;
    }

    $.ajax(
        {
          url: "test_suite.json",
          data:{"id":active_id},
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
              var data_obj = data.rows

              // 赋值
              $("#id").val(active_id);
              $("#name").val(data_obj.name);
              $("#run_type").val(data_obj.run_type);
              $("#description").val(data_obj.description);

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
function delete_test_suite(active_id)
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
            url: "delete_test_suite",
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

// 提交表单
function add_test_suite()

  {

//    var $form = $("#new_test_suite");
//
//    var data = $form.data('bootstrapValidator');
//    if (data) {
//    // 修复记忆的组件不验证
//        data.validate();
//
//        if (!data.isValid()) {
//            return false;
//        }
//    }

    // 异步提交数据到action/add_action.php页面
    $.ajax(
        {
          url: "/add_test_suite.json",
          data:{"run_type":$("#run_type").val(),"name":$("#name").val(),"description":$("#description").val()},
          type: "post",
          beforeSend:function()
          {
            $("#tip").html("<span style='color:blue'>正在处理...</span>");
            return true;
          },
          success:function(data)
          {
            var data=data;
            if(data.code == 200)
            {
             alert('新增成功，请关联用例!');
             window.location.href=('/attach_test_batch?test_suite_id='+data.ext);
            }
            else
            {
              alert(data.msg);
            }
          },
          error:function()
          {
            alert('请求出错');
          },
          complete:function()
          {
            $('#acting_tips').hide();
          }
        });

    return false;
  }

//function runtest1(id){
//alert(id);
//}

 function runtest(test_suite_id){
         $.ajax(
        {
          url: "/runtest.json",
          data:{"id":test_suite_id,"type":"test_suite"},
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

function copy_test_suite(test_suite_id){
         $.ajax(
        {
          url: "/copy_test_suite",
          data:{"id":test_suite_id},
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