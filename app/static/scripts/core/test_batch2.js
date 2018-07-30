function getDevices(){
      $.ajax(
            {
              url: "/getDevicesList.json",
              data:{},
              type: "get",
              dataType:"json",
              beforeSend:function()
              {
                return true;
              },
              success:function(data)
              {

                  var ipList=data["msg"]
                  $("#ipList").html("");
                   var option_group='';
                   var optionInit='<option value="">-请选择-</option>'
                   for (var j=0;j<ipList.length;j++){
                       var selectdata=ipList[j];
                       var ip=ipList[j]["ip"]
                       var model=ipList[j]["model"]
                       var option='<option value="'+ip+'">'+model+'</option>';
                       option_group+=option;
                  }
                  $("#ipList").append(optionInit);
                  $("#ipList").append(option_group);

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
////检查下拉框选中id
//function get_multiple_select_value(objSelectId){
//    var objSelect = document.getElementById(objSelectId);
//    var length = objSelect.options.length;
//    var value = '';
//    for(var i=0;i<length;i++){
//        if(objSelect.options[i].selected==true){
//        if(value==''){
//        value = objSelect.options[i].value;
//        }else{
//        value = value+','+objSelect.options[i].value;}
//
//        }
//    }
//    return value;
//}
//指定设备
function run_test_case_Ip(test_case_id){
    //获取校验规则Id
    ipVal=get_multiple_select_value("ipList")
     $.ajax(
        {
          url: "/runtest.json",
          data:{"id":test_case_id,"ipVal":ipVal,"type":"test_case"},
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

// submit form
function submitAddForm() {
   $("#new_test_case").validate();
   $.validator.setDefaults({
        submitHandler: function() {
            document.getElementById("new_test_case").submit();
    }
});
   }

function initPage(test_case_id){
    var oTable = new TableInit(test_case_id);
    oTable.Init(test_case_id);
    get_test_case_info(test_case_id);
}

var TableInit = function (test_case_id) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_test_batch2').bootstrapTable({
            url: '/test_batch.json',         //请求后台的URL（*）
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
            pageList: [10, 25, 50, 100,500],        //可供选择的每页的行数（*）
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
                field: 'test_suite_id',
                title: '用例集ID'
            }, {
                field: 'name',
                title: '名称'
            }, {
                field: 'browser_type',
                title: '浏览器类型'
            }
            , {
                field: 'status',
                title: '执行状态',
                formatter: function(value,row,index) {
            //通过判断单元格的值，来格式化单元格，返回的值即为格式化后包含的元素
            var a = "";
                if(value == "1-执行成功") {
                    var a = '<span style="color:#00ff00">'+value+'</span>';
                }else if(value == "2-执行失败"){
                    var a = '<span style="color:#0000ff">'+value+'</span>';
                }else if(value == "0-待执行") {
                    var a = '<span style="color:#FF0000">'+value+'</span>';
                }else{
                    var a = '<span>'+value+'</span>';
                }
                return a;
        }
            }, {
                field: 'steps',
                title: '步骤'
            }, {
                field: 'runtime',
                title: '执行时间'
            }, {
                field: 'screenshot',
                title: '截图',
                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/view_test_suite_screenshot?type=test_case&test_batch_id='+test_case_id+'&id='+ row.id + '\')">截图</a> ';
                        var b = '<a href="javascript:;" onclick="run_test_batch_record(\''+row.id+'\',\''+row.test_case_id+ '\')">重跑</a> ';
                        return b+a;
                        }
            }, {
                field: 'message',
                title: '描述'
            }
                ]
        });
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
             var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            id: test_case_id,
            status : $("#selectStatus").val(),
            name : $('#casename').val(),
            type:"test_case",
            browser_type : $('#browser_type').val()
        };
        return temp;
    };
    return oTableInit;
};


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


 // 编辑表单
function get_test_case_info(active_id)
  {

    if(!active_id)
    {
      alert('Error！');
      return false;
    }

    $.ajax(
        {
          url: "/test_case.json",
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
              var data_obj = data.rows;

              // 赋值
              $("#id").val(active_id);
              $("#name").val(data_obj.name);
              $("#module").val(data_obj.module);
              $("#steps").val(data_obj.steps);
              $("#description").val(data_obj.description);
              $("#type").val(data_obj.isPublic);
              if (data_obj.module=='android'){
                  getDevices();
              }else{
                   $("#ipList").hide();
                   $("#btn_runIp_test").hide();
                   $("#ipListLabel").hide();
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

    return false;
  }


function searchTestBatch2(test_case_id){
    var $tb_departments = $('#tb_test_batch2');
    $tb_departments.bootstrapTable('refresh', {url: '/test_batch.json',data:{id: test_case_id,status : $("#selectStatus").val(), name : $('#casename').val(),type:'test_case'}});
}

//
//function selectOnchang(obj){
////获取被选中的option标签选项
//var value = obj.options[obj.selectedIndex].value;
////alert(value);
//}

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

function return_page(test_batch_id,type){
if(type=='test_case'){window.location.href=('/test_case_runhistory?id='+test_batch_id);
}else{window.location.href=('/test_batch_detail?test_suite_id='+test_batch_id);}

}


 function run_test_batch_record(rowid,test_case_id){
         $.ajax(
        {
          url: "/runtest.json",
          data:{"id":rowid,"type":"test_batch","test_case_id":test_case_id},
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