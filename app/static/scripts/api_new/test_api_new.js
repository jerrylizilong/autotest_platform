
//// submit form
//function submitAddForm() {
//   $("#new_test_api").validate();
//   $.validator.setDefaults({
//        submitHandler: function() {
//            document.getElementById("new_test_api").submit();
//    }
//});
//   }



$(function () {
    //初始化可编辑表格
//     modelEdit();

//     //获取测试ip 列表
//     getApiUrl();

    var oTable = new TableInit();
    oTable.Init();
});



var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_test_api').bootstrapTable({
            url: '/test_api_new.json',         //请求后台的URL（*）
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
                title: 'id',
                width : '10'
            }, {
                field: 'product',
                title: '所属产品',
                width : '20'
            }, {
                field: 'module',
                title: '模块',
                width : '20'
            }, {
                field: 'name',
                title: '接口名称',
                width : '20'
            }, {
                field: 'url',
                title: '接口地址',
                width : '20'
            },
             {
                field: 'operate',
                title: '操作',
//                align: 'center',
                formatter: function (value, row, index) {
                        var a = '<a href="javascript:;" onclick="window.location.href=(\'/edit_test_api_new?id='+ row.id + '\')">编辑</a> ';
                         var d = '<a href="javascript:;" onclick="window.location.href=(\'/test_api_new_test?id='+ row.id + '\')">测试</a> ';
                        var b = '<a href="javascript:;" onclick="delete_test_api_new(\'' + row.id + '\')">删除</a> ';
                        var div = "<div style='width:30px;'>"+a+d+b+"</div>";
                        return div;
                        }
                },
             {
                field: 'osign_list',
                title: '加密参数列表',
                width : '50'
            },{
                field: 'description',
                title: '备注'
//                width : '50'
            },
                {
                field: 'paras',
                title: '参数列表'
//                width : '50'
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
                window.location.href=('/add_test_api');
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
            module: $("#module").val(),
            type:"test_api"
        };
        return temp;
    };
    return oTableInit;
};


function searchTestCase(){
    var name=$('#name').val();
    var product=$('#product').val();
    var module=$('#module').val();
   $('#tb_test_api').bootstrapTable('refresh', {url: '/test_api_new.json',query:{'name': name,'product':product,'module':module}});
}



function addApiNew(){
       var paras = getParaTable();
       $.ajax(
        {
          url: "/add_test_api_new.json",
          data:{'name':$('#name').val(),'product':$('#product').val(),'module':$('#module').val(),'url':$('#url').val(),'osign_list':$('#osignList').val(),'description':$('#description').val(),'paras':paras},
          type: "post",
          async: false,
//          dataType:"json",
          beforeSend:function()
          {
            return true;
          },
          success:function(data)
          {
            console.log(data);
            console.log(data['code']);
            if(data['code']==200)
            {
                alert('新增成功！');
                window.location.href=('/test_api_new');
              }
            else
            {
//              $("#tip").html("<span style='color:red'>失败，请重试</span>");
              alert('失败，请重试');
            }
          },
          error:function()
          {
            alert('请求出错');
//            document.getElementById('btn_back').click();
          },
          complete:function()
          {
            // $('#tips').hide();
//           document.getElementById('btn_back').click();
                window.location.href=('/test_api_new');
          }
        });
}



function update_api_new(id){
       var paras = getParaTable();
       $.ajax(
        {
          url: "/update_test_api_new.json",
          data:{'id':id,'name':$('#name').val(),'product':$('#product').val(),'module':$('#module').val(),'url':$('#url').val(),'osign_list':$('#osign_list').val(),'description':$('#description').val(),'paras':paras},
          type: "post",
//          dataType:"json",
          beforeSend:function()
          {
            return true;
          },
          success:function(data)
          {
            console.log(data);
            console.log(data['code']);
            if(data['code']==200)
            {
                alert('保存成功！');
//                document.getElementById('btn_back').click();
                window.location.href=('/test_api_new');
              }
            else
            {
//              $("#tip").html("<span style='color:red'>失败，请重试</span>");
              alert('失败，请重试');
            }
          },
          error:function()
          {
            alert('请求出错');
//            document.getElementById('btn_back').click();
          },
          complete:function()
          {
            // $('#tips').hide();
           window.location.href=('/test_api_new');
//            document.getElementById('btn_back').click();
          }
        });
}






 // 编辑表单
function get_api_info(active_id)

  {
    if(!active_id)
    {
      alert('Error！');
      return false;
    }
    $.ajax(
        {
          url: "/test_api_new.json",
          data:{"id":active_id,'type':'all'},
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
              var data_obj = data.rows[0]
              console.log(data_obj.paras);
              var paras = JSON.parse(data_obj.paras.replace(/'/g, '"'));
//              var paras = JSON.parse(data_obj.paras);
              console.log(paras);
              console.log(typeof(paras));
              var paras = JSON.parse(paras);
              console.log(typeof(paras));
              console.log(paras['appId']);
//              var paras = data_obj.paras;
              $("#name").val(data_obj.name);
              $("#description").val(data_obj.description);
              $("#url").val(data_obj.url);
              $("#product").val(data_obj.product);
              $("#module").val(data_obj.module);
              $("#osign_list").val(data_obj.osign_list);
              setParaTable(paras);
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
function delete_test_api_new(active_id)
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
            url: "/delete_test_api_new",
            data:{"id":active_id},
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

function run_test_api(id){
     $.ajax(
        {
          url: "/runurltest.json",
          data:{"id":id},
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
              window.location.href=('/test_api_batch_case_detail?batch_id=1&url_id='+id+'&id='+data.test_case_id);
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

//
function runTest(){
      var id=$("#urlId").val();
      var apiUrl=$('#apiUrl option:selected') .val();
      $.ajax(
        {
          url: "/runurltest.json",
          data:{"id":id,"apiUrl":apiUrl},
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
//              alert('success!');
              window.location.href=('/test_api_case_run?batch_id=1&url_id='+id+'&id='+data.test_case_id);
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


function readPara(){
     var url =  $("#paraList").val();
     $.ajax(
            {
              url: "/split_test_api_url.json",
              data:{'url':url},
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
                 console.log(data);
                 $("#name").val(data['url']['url']);
                 $("#url").val(data['url']['url']);
                 $("#module").val(data['url']['url']);
                 $("#description").val(data['url']['url']);
                 $("#product").val(data['url']['type']);
                 setParaTable(data['paras']);
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


function setProduct(type)
{
 setSelectOption('product',type);
}

function setSelectOption(selectObj, value) {
     selectObj = document.getElementById(selectObj);
     // 清空选项
//     console.log(value);
//     console.log(selectObj.options);
     for (var i =0;i< selectObj.options.length;i++) {
//             console.log(selectObj.options[i].value,value);
             if(selectObj.options[i].value==value)  {
             selectObj.options[i].selected = true;
             }
         }
 }


function setParaTable(para_info){
    var tbodies= $("#para_table");
    console.log(para_info);
    for (var key in para_info){
//        console.log(key);
//        console.log(para_info[key]);
        var tr = '<tr>';
        tr+= "<td class='hidden-phone'><a class='para_name' data-placement='right'>"+key+"</a></td>";
        tr+= "<td class='hidden-phone'><a class='para_value' data-placement='right'>"+para_info[key]+"</a></td>";
        if (key.indexOf("Ver") != -1 || key.indexOf("Type") != -1 || key.indexOf("Platform") != -1){
            tr+= "<td class='hidden-phone'><input class='isParamized' type='checkbox' checked='checked'></td>";
        }else{
            tr+= "<td class='hidden-phone'><input class='isParamized' type='checkbox'></td>";
        }
        tr += "<td class='hidden-phone'><input class='paramized_value' type='text' value='{"+key+"}'></td>";
        tr += '</tr>';
//        console.log(tr);
        tbodies.append(tr);
//        console.log(tbodies);
    }
}

function getParaTable(){
    var tbodies= $("#para_table");
    var para_name_list = document.getElementsByClassName('para_name');
    var para_value_list = document.getElementsByClassName('para_value');
    var isParamized_list = document.getElementsByClassName('isParamized');
    var paramized_value_list = document.getElementsByClassName('paramized_value');

    var paras = {};
    for (var i=0;i< para_name_list.length;i++){
        console.log(para_name_list[i].text+para_value_list[i].text+isParamized_list[i].checked+paramized_value_list[i].value);
        if (isParamized_list[i].checked){
            paras[para_name_list[i].text]=paramized_value_list[i].value;
        }else{
            paras[para_name_list[i].text]=para_value_list[i].text;
        }
    }
    console.log(paras);
    var jsonString = JSON.stringify(paras);
        console.log(jsonString);
    return jsonString;
}