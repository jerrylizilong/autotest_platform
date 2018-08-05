

$(function () {

//    1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

//    //2.初始化Button的点击事件
//    var oButtonInit = new ButtonInit();
//    oButtonInit.Init();

});


// submit form
function addHub() {
   $("#new_hub").validate();
   $.ajax(
          {
            url: "/add_hub.json",
            data:{"host":$("#host").val(), "port":$("#port").val(),"status":$("#status").val()},
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
                alert('恭喜，成功！');
                $("#tip").html("<span style='color:blueviolet'>恭喜，新增成功！</span>");
                window.location.href=('/testhubs');
              }
              else
              {
                $("#tip").html("<span style='color:red'>失败，请重试</span>");
                alert('失败，请重试: '+data.msg);
                window.location.href=('/add_hub');
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


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_hubs').bootstrapTable({
            url: '/search_hubs.json',         //请求后台的URL（*）
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
                field: 'ip',
                title: 'ip'
            }, {
                field: 'port',
                title: 'port'
            },
             {
                field: 'status',
                title: '是否打开',
                formatter: function(value,row,index) {
            //通过判断单元格的值，来格式化单元格，返回的值即为格式化后包含的元素
            var b = "";
                if(value == "1") {
                    var b = '<span style="color:#00ff00">开启</span>';
                }else if(value == "0") {
                    var b = '<span style="color:#FF0000">关闭</span>';
                }else{
                    var b = '<span>'+value+'</span>';
                }
                return b;
                        }
            },
             {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_hub?id='+ row.id + '\')">编辑</a> ';
                        return a;
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
            name: $("#name").val()
//            module: $("#selectModule").val(),
//            type:"test_cases"
        };
        return temp;
    };
    return oTableInit;
};


function searchHubs(){
//    alert(1)
    var $tb_departments = $('#tb_hubs');
    $tb_departments.bootstrapTable('refresh', {url: '/search_hubs.json',data:{name:$("#name").val() }});
}




function check_hubs(){
  $.ajax({
  url: '/check_hubs.json',
  method: 'get',

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

