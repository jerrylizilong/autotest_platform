$(function () {
    var id=$("#id").val();
    get_info(id);
    fullurl();
});



//查找apiUrl
function getApiHostList(type){
    $.ajax(
            {
              url: "/test_api_host.json",
              data:{'type':type},
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
                 $("#host_id").html("");
                 var option_group='';
                 for (var i=0;i<data.rows.length;i++){
                       var selectdata=data.rows[i];
                       var option='<option value="'+i+'">'+data.rows[i]+'</option>';
                       console.log(option);
                       option_group+=option;
                       console.log(option_group);
                 }
                 console.log(option_group);
                  $("#host_id").append(option_group);
                  $("#host").val(data.rows[0]);
                  fullurl();
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
function get_info(active_id)
  {
    if(!active_id)
    {
      alert('Error！');
      return false;
    }
    $.ajax(
        {
          url: "/test_api_new.json",
          data:{"id":active_id,'type':'default'},
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
              console.log(paras);
              $("#name").val(data_obj.name);
//              $("#product").val(data_obj.product);
              $("#description").val(data_obj.description);
              $("#url").val(data_obj.url);
              $("#osign_list").val(data_obj.osign_list);
              console.log(paras);
              addBody(paras);
              getApiHostList(data_obj.product);
              reosign();
//              fullurl();


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

function addBody(content){

    $("#tbody").html("");
    var tbody=document.getElementById('tbody');
    console.log('body is:'+tbody);
//    data =(new Function("","return "+content))();
    var data = content;
    for(var key in data){
      var tr=document.createElement('tr');
      var tdname=document.createElement('td')
      var tdvalue=document.createElement('td')
      tdvalue.contentEditable="true";
      tdname.innerHTML=key;
      tdvalue.innerHTML=data[key];
      tr.appendChild(tdname);
      tr.appendChild(tdvalue);
      tbody.appendChild(tr);

    }

console.log('body is:'+tbody);

}

//
// // 编辑表单
//function runtest()
//  {
//    var mytable = document.getElementById('paraTable');
//    var url = $("#url").val();
//    var context={};
//    for(var i=1,rows=mytable.rows.length; i<rows; i++){
//        context[mytable.rows[i].cells[0].innerHTML]=mytable.rows[i].cells[1].innerHTML;
//    }
//    var context = JSON.stringify(context);
//
//    $.ajax(
//        {
//          url: "/test_api_new.json",
//          data:{"url":url,"context":context},
//          type: "get",
//          dataType:"json",
//          beforeSend:function()
//          {
//            return true;
//          },
//          success:function(data)
//          {
//            if(data)
//            {
//              // 解析json数据
//              var data = data;
////              alert(data);
//              var data_obj = data.rows[0];
////              alert(data_obj);
//              // 赋值
////              $("#url").val(url+'?'+paraList);
//              $("#response").val(data_obj.response);
//              $("#content").val(data_obj.content);
//
//              }
//            else
//            {
//              $("#tip").html("<span style='color:red'>失败，请重试</span>");
//             // alert('操作失败');
//            }
//          },
//          error:function()
//          {
//            alert('请求出错');
//          },
//          complete:function()
//          {
//            // $('#tips').hide();
//          }
//        });
//
//    return false;
//  }


 // 编辑表单
function runapitest()
  {
    fullurl();
    var fullurlcontext = $("#fullurlcontext").val();
    $.ajax(
        {
          url: "/test_api_new_run.json",
          data:{"url":fullurlcontext},
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
//              alert(data);
              var data_obj = data.rows[0];
//              alert(data_obj);
              // 赋值
//              $("#url").val(url+'?'+paraList);
              $("#response").val(data_obj.response);
              $("#content").val(data_obj.content);

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



// 编辑表单
function reosign()
  {
    var mytable = document.getElementById('paraTable');
    var context={};
    for(var i=1,rows=mytable.rows.length; i<rows; i++){
//        context.push(mytable.rows[i].cells[0].innerHTML:mytable.rows[i].cells[1].innerHTML,);
        context[mytable.rows[i].cells[0].innerHTML]=mytable.rows[i].cells[1].innerHTML;
    }
    var context = JSON.stringify(context);
    var osign_list = $("#osign_list").val();
    $.ajax(
        {
          url: "/test_api_reosign_new.json",
          data:{"osign_list":osign_list,"context":context},
          type: "get",
          dataType:"json",
          beforeSend:function()
          {
            return true;
          },
          success:function(data)
          {
            if(data && data.code == '200')
            {
              // 解析json数据
              var data_obj = data.rows[0]
              console.log(data_obj.context);
              var paras = JSON.parse(data_obj.context.replace(/'/g, '"'));
              addBody(paras);
              }
            else
            {
              $("#tip").html("<span style='color:red'>失败，请重试</span>");
              alert('重签名失败，请确认参数中是否有签名字段');
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

function changehost(){
    var selectedIndex = document.getElementById('host_id').selectedIndex;
    console.log(selectedIndex);
    var host = document.getElementById('host_id').options[selectedIndex].text;
    console.log(host);
    $("#host").val(host);
    fullurl();
}

//function refreshhost(apiUrl){
//    $("#host").val(apiUrl);
//    $("#apiUrl").val(apiUrl);
//}

function fullurl(){
    var host = $("#host").val();
    var url = $("#url").val();
    var mytable = document.getElementById('paraTable');
    var context='?';
    for(var i=1,rows=mytable.rows.length; i<rows; i++){
        if(i>1){
            context = context+'&' + mytable.rows[i].cells[0].innerHTML+'='+mytable.rows[i].cells[1].innerHTML;
        }
        else{
            context = context + mytable.rows[i].cells[0].innerHTML+'='+mytable.rows[i].cells[1].innerHTML;
        }
    }

    $("#fullurlcontext").val(host+url+context);
}


 // 刷新前置参数
function refresh_prepose(batch_id,url_id)
  {
    var url = $("#host").val();
    $.ajax(
        {
          url: "/test_api_refresh_prepose.json",
          data:{"url":url,"url_id":url_id,"batch_id":batch_id},
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
//                alert('刷新前置参数成功！');
                window.location.reload();
                alert('刷新前置参数成功！');
                refreshhost(url);
              }
            else
            {
//              $("#tip").html("<span style='color:red'>失败，请重试</span>");
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
