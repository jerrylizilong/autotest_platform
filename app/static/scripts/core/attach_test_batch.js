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

// submit form
function submitAddForm() {
   $("#new_test_case").validate();
   $.validator.setDefaults({
        submitHandler: function() {
            document.getElementById("new_test_case").submit();
    }
});
   }

function initPage(test_suite_id){
    var oTable = new TableInit(test_suite_id);
    oTable.Init(test_suite_id);
    get_edit_info(test_suite_id);


}
//
//function iniImage(lenth, i, pro){
//if (lenth>1){
//
//}
//else{
//alert("only one page!");
//}
//}



var TableInit = function (test_suite_id) {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_test_batch1').bootstrapTable({
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
            },{
                field: 'module',
                title: '模块'
            },{
                field: 'name',
                title: '名称'
            }, {
                field: 'steps',
                title: '步骤'
            }, {
                field: 'description',
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
            id: test_suite_id,
            module : get_multiple_select_value( "module"),
            name : $('#casename1').val(),
            type: 'unattach'
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

//
//function get_multiple_select_value(objSelectId){
//var objSelect = document.getElementById(objSelectId);
//var length = objSelect.options.length;
//var value = '';
//for(var i=0;i<length;i++){
//    if(objSelect.options[i].selected==true){
//    if(value==''){
//    value = objSelect.options[i].value;
//    }else{
//    value = value+','+objSelect.options[i].value;}
//
//    }
//}
//return value;
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
              if (data_obj.run_type=='Android'){
                  getDevices();
              }else{
                   $("#ipList").hide();
//                   $("#btn_runIp_test").hide();
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


function searchTestBatch1(test_suite_id){
    var $tb_departments = $('#tb_test_batch1');
    $tb_departments.bootstrapTable('refresh', {url: '/test_case.json',data:{id: test_suite_id,status : $("#selectStatus1").val(), name : $('#casename1').val(),type:'unattach'}});
}

//
//function selectOnchang(obj){
////获取被选中的option标签选项
//var value = obj.options[obj.selectedIndex].value;
////alert(value);
//}

function attachTestCase(test_suite_id){
   var  ipVal=get_multiple_select_value("ipList");
   var browser_list=get_multiple_select_value("browserList");
    var $tb_departments = $('#tb_test_batch1');
    var a= $tb_departments.bootstrapTable('getSelections');
    var datarow = '';
    for(var i=0;i<a.length;i++){
//        alert(a[i].id);
        datarow = datarow+','+a[i].id;
        }
//    alert(test_suite_id);
//    alert(datarow);
    if(a.length>0){
         $.ajax(
        {
          url: "/attach_test_batch.json",
          data:{"test_suite_id":test_suite_id,"ipVal":ipVal,"browser_list":browser_list,"datarow":datarow},
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
}else{
   alert('no row is selected!');
   }
}


//
// function removeOptions(selectObj)
// {
// if (typeof selectObj != 'object')
// {
// selectObj = document.getElementById(selectObj);
// }
// // 原有选项计数
// var len = selectObj.options.length;
// for (var i=0; i < len; i++) {
// // 移除当前选项
// selectObj.options[0] = null;
// }
// }
// /*
// * @param {String || Object]} selectObj 目标下拉选框的名称或对象，必须
// * @param {Array} optionList 选项值设置 格式：[{txt:'北京', val:'010'}, {txt:'上海', val:'020'}] ，必须
// * @param {String} firstOption 第一个选项值，如：“请选择”，可选，值为空
// * @param {String} selected 默认选中值，可选
// */
// function setSelectOption(selectObj, optionList, firstOption, selected) {
// if (typeof selectObj != 'object')
// {
// selectObj = document.getElementById(selectObj);
// }
// // 清空选项
// removeOptions(selectObj);
// // 选项计数
// var start = 0;
// // 如果需要添加第一个选项
// if (firstOption) {
// selectObj.options[0] = new Option(firstOption, '');
// // 选项计数从 1 开始
// start ++;
// }
// var len = optionList.length;
// for (var i=0; i < len; i++) {
// // 设置 option
// selectObj.options[start] = new Option(optionList[i].txt, optionList[i].val);
// // 选中项
// if(selected == optionList[i].val)  {
// selectObj.options[start].selected = true;
// }
// // 计数加 1
// start ++;
// }
// }
//
//var moduleArr = [];
//moduleArr['Android'] =
//[
// {txt:'Android', val:'android'}
// ];
//moduleArr['普通用例'] =
//[
// {txt:'setting', val:'setting'},
// {txt:'data', val:'data'},
// {txt:'system', val:'system'},
// {txt:'userBehavior', val:'userBehavior'},
// {txt:'monitor', val:'monitor'},
//  {txt:'H5管理后台', val:'H5_back'},
//  {txt:'H5平台', val:'H5_front'}
// ];
//function setModule(type)
//{
// setSelectOption('module', moduleArr[type], '-请选择-');
//}
