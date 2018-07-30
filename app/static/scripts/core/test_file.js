
// submit form
function submitAddForm() {
   $("#new_test_file").validate();
   $.validator.setDefaults({
        submitHandler: function() {
            document.getElementById("new_test_file").submit();
    }
});
   }



$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();
//
//    //2.初始化Button的点击事件
//    var oButtonInit = new ButtonInit();
//    oButtonInit.Init();

});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_body').bootstrapTable({
            url: '/search_test_file.json',         //请求后台的URL（*）
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
                field: 'name',
                title: '名称'
            }, {
                field: 'filePath',
                title: '脚本名称'
            },
             {
                field: 'description',
                title: '描述'
            },{
                field: 'runStatus',
                title: '执行状态',
                formatter: function(value,row,index) {
                    //通过判断单元格的值，来格式化单元格，返回的值即为格式化后包含的元素
                        var a = "";
                            if(value == "0") {
                                var a = '<span>未执行</span>';
                            }else if(value == "1"){
                                var a = '<span>待执行</span>';
                            }else if(value == "2") {
                                var a = '<span>正在执行</span>';
                            }else{
                                var a = '<span>'+value+'</span>';
                            }
                            return a;
                    }
              },
             {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: function (value, row, index) {
                        if (row.runStatus=='2'){
                                var aa = '<a href="javascript:;" onclick="openLocust()">查看</a> ';
                                var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_test_file?id='+ row.id + '\')">编辑</a> ';
                                var b = '<a href="javascript:;" onclick="delete_test_file(\'' + row.id + '\',\'' + row.filePath + '\')">删除</a> ';
                                var c = '<a href="javascript:;" onclick="run_test_file(\'' + row.id + '\',\'' + row.filePath + '\')">执行</a> ';
                                 var d = '<a href="javascript:;" onclick="load_test_file(\'' + row.id + '\',\'' + row.filePath + '\')">下载</a> ';
                                return aa+a+b+c+d;
                        }else{
                          var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_test_file?id='+ row.id + '\')">编辑</a> ';
                            var b = '<a href="javascript:;" onclick="delete_test_file(\'' + row.id + '\',\'' + row.filePath + '\')">删除</a> ';
                            var c = '<a href="javascript:;" onclick="run_test_file(\'' + row.id + '\',\'' + row.filePath + '\')">执行</a> ';
                             var d = '<a href="javascript:;" onclick="load_test_file(\'' + row.id + '\',\'' + row.filePath + '\')">下载</a> ';
                            return a+b+c+d;
                        }
                        }
                }
                ]
        });
    };



function operateFormatter(value, row, index) {
            return [
                '<button type="button" class="RoleOfEdit btn btn-default  btn-sm" style="margin-right:15px;">编辑</button>',
                '<button type="button" class="RoleOfDelete btn btn-default  btn-sm" style="margin-right:15px;">删除</button>'
            ].join('');
        }

window.operateEvents = {
            'click .RoleOfEdit': function (e, value, row, index) {
                window.location.href=('/add_test_file');
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
            name: $("#name").val()
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

function search(){
    var name=$('#name').val();
   $('#tb_body').bootstrapTable('refresh', {url: '/search_test_file.json',query:{'name': name}});
}





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
          url: "/search_test_file.json",
          data:{"id":active_id,"type":"test_case"},
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
              var data_obj = data.rows[0]
              // 赋值
              $("#id").val(active_id);
              $("#name").val(data_obj.name);
              $("#filePath").val(data_obj.filePath);
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
function delete_test_file(active_id,filePath)
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
            url: "/delete_test_file",
            data:{"id":active_id,"filePath":filePath, "act":"del"},
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

            }
          });

    }
    return false;
  }
 //执行脚本
function run_test_file(active_id,filePath)
  {

      if(!active_id)
      {
        alert('Error！');
        return false;
      }
      $.ajax(
          {
            url: "/run_test_file",
            data:{"id":active_id,"filePath":filePath, "act":"run"},
            type: "post",
            beforeSend:function()
            {
              $("#tip").html("<span style='color:blue'>正在处理...</span>");
              return true;
            },
            success:function(data)
            {
              if(data ==1)
              {
                alert('恭喜，执行成功！');
                //执行成功，打开新窗口
//                window.open("http://localhost:8089/")
                $("#tip").html("<span style='color:blueviolet'>恭喜，执行成功！</span>");


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

            }
          });

    return false;
  }



//下载脚本
function load_test_file(active_id,filePath){
       window.location.href="/load_test_file?id="+active_id+"&filePath="+filePath

}

//启动locust
function openLocust(){
   window.open("http://172.16.100.55:8089/")
}