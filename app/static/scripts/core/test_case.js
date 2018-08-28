
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

function openEditStepWindow(){

    document.getElementById('editStep').style.display='block';
    document.getElementById('fade').style.display='block';
    var options = keywordOption();
//    alert(options);

    var content = $("#steps").val();
    if(content==''){content='Chrome'}
    $("#step").val();
    $("#step").val(content);
    var steps = content.split(',');
    var steprows = steps.length;

    for(var i=0;i<steprows;i++){
        addBody(steps[i],i+1,options,0);
    }
}

function closeEditStepWindow(){

    var tb_step=document.getElementById('stepsTable');
    var tbodies= document.getElementsByTagName("tbody");
    tb_step.removeChild(tbodies[0]);
    var tbody=document.createElement('tbody');
    tb_step.appendChild(tbody)
    document.getElementById('editStep').style.display='none';
    document.getElementById('fade').style.display='none';

}


function addBody(content,order,options,isInsert){
//    alert(options);

    var tbody=document.getElementsByTagName('tbody')[0];
//    alert(isInsert);
    if(isInsert==1){
//        alert('insert new:'+order);
        var table = document.getElementById('stepsTable');
        var tr=table.insertRow(order);
        var ran = Math.floor(Math.random()*(100-10+1)+10);
        order = 'new_'+order+ran;
    }else{
        var tr=document.createElement('tr');
    }

    var words = content.split('|');
    var tdoperate=document.createElement('td')
    var addBtn=document.createElement('a');
    var delBtn=document.createElement('a');
    var copyBtn=document.createElement('a');

    addBtn.setAttribute("onclick","addRow(this);");
    addBtn.setAttribute("class","btn");
    var addIcon=document.createElement('i');
    addIcon.setAttribute("class","fa fa-plus");
    addBtn.appendChild(addIcon);

    delBtn.setAttribute("onclick","delRow(this);");
    delBtn.setAttribute("class","btn");
    var delIcon=document.createElement('i');
    delIcon.setAttribute("class","fa fa-minus");
    delBtn.appendChild(delIcon);

    copyBtn.setAttribute("onclick","copyRow(this,'"+order+"');");
    copyBtn.setAttribute("class","btn");
    var copyIcon=document.createElement('i');
    copyIcon.setAttribute("class","fa fa-clone");
    copyBtn.appendChild(copyIcon);

    tdoperate.appendChild(addBtn);
    tdoperate.appendChild(delBtn);
    tdoperate.appendChild(copyBtn);
    tr.appendChild(tdoperate);

    var tdvalue=document.createElement('td')
//    tdvalue.innerHTML=words[0];
    var select = selectOptions(options,words[0])
    select.setAttribute("id","td_keyword_"+order);
    select.setAttribute("onchange","if(this.value != '') changeValue(this,'"+order+"');");
    tdvalue.appendChild(select);
    tdvalue.setAttribute("onchange","change(this,"+order+");");
//    $("#td_keyword_"+order).find("option[value='"+words[0]+"']").attr("selected",true);
    tr.appendChild(tdvalue);
    if(words.length==1){
      for(var i=0;i<4;i++){
      var tdvalue=document.createElement('td')
      tdvalue.contentEditable="true";
      tdvalue.setAttribute("class","td_para_"+order);
      tdvalue.setAttribute("onKeyUp","change(this,'"+order+"');");
      tdvalue.innerHTML='';
      tr.appendChild(tdvalue);
    }
    }else{

    var steps = words[1].split('@@');
    for(var i=0;i<4;i++){
      var tdvalue=document.createElement('td')
      tdvalue.contentEditable="true";
      tdvalue.setAttribute("class","td_para_"+order);
      tdvalue.setAttribute("onKeyUp","change(this,"+order+");");
      if(i<steps.length){tdvalue.innerHTML=steps[i];}
      else{tdvalue.innerHTML='';}
       tr.appendChild(tdvalue);
    }

    }
    var tdvalue=document.createElement('td')
    tdvalue.contentEditable="true";
    tdvalue.setAttribute("class","td_content");
    tdvalue.setAttribute("id","td_content_"+order);
    if(content!=''){
        tdvalue.innerHTML=content;
        }else{
        var newkeyword = document.getElementById('td_keyword_'+order);
        tdvalue.innerHTML=newkeyword.options[newkeyword.selectedIndex].value;
        }
    tr.appendChild(tdvalue);

     if(isInsert==0){tbody.appendChild(tr);}
console.log('body is:'+tbody);

}

function change(obj,order){
obj.textContent.change;
var content = document.getElementById('td_content_'+order);
var keyword = document.getElementById('td_keyword_'+order);
var paras= document.getElementsByClassName("td_para_"+order);
var newvalue = keyword.options[keyword.selectedIndex].value;
var methodSelect = paras[0].getElementsByClassName('method');
//alert(methodSelect.length);
if(methodSelect.length==1){
    method = methodSelect[0].options[methodSelect[0].selectedIndex].value;
}else{ method = paras[0].textContent;}
//alert(method);
if(method!=''){
    newvalue = newvalue+'|'+method;
}

for(var i=1;i<paras.length;i++){
    if(paras[i].textContent!=''){
        newvalue = newvalue+'@@'+paras[i].textContent;
        }
    }

content.innerHTML = newvalue;
}

function SaveAndCloseEditStepWindow(){
    var stepsvalue = '';
    var contents= document.getElementsByClassName("td_content");
    for(var i=0;i<contents.length;i++){
        if(i!=0){stepsvalue = stepsvalue+','+contents[i].textContent;}
        else{stepsvalue = stepsvalue+contents[i].textContent;}
    }

//    alert(stepsvalue);
    $("#steps").val(stepsvalue);
    closeEditStepWindow();

}


function selectOptions(options,defaultOption){
//alert(options);
var select = document.createElement('select');
for(var i=0;i<options.length;i++){
    var option = document.createElement('option');
    option.value = options[i];
    option.text = options[i];
    if(options[i]==defaultOption){
        option.setAttribute("selected","true");
    }
    select.appendChild(option)
}
return select;
}


function keywordOption(){

var options = []

 $.ajax(
    {
      url: "/test_keywords_options.json",
      type: "get",
      dataType:"json",
      async : false,
      beforeSend:function()
      {
        return true;
      },
      success:function(data)
      {
//        alert(data.rows);
        options= data.rows;

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
//alert('options are :'+options);
return options;
}


function getPublicFunctions(){

var cases = []

 $.ajax(
    {
      url: "/test_public_test_cases.json",
      type: "get",
      dataType:"json",
      async : false,
      beforeSend:function()
      {
        return true;
      },
      success:function(data)
      {
//        alert(data.rows);
        cases= data.rows;

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
//alert('options are :'+options);
return cases;
}


function addRow(ojb){
    var n=ojb.parentNode.parentNode.rowIndex+1;
//    alert(n);
    var options = keywordOption();
    addBody('',n,options,1);
}


function delRow(ojb){
var n=ojb.parentNode.parentNode.rowIndex;
var table = document.getElementById('stepsTable');
var tr=table.deleteRow(n);
}



function copyRow(ojb,order){
    var n=ojb.parentNode.parentNode.rowIndex+1;
    var content = document.getElementById('td_content_'+order).textContent;
//    alert(content);
    var options = keywordOption();
    addBody(content,n,options,1);
}

function changeValue(obj,order){
//setModule(obj.options[obj.selectedIndex].value);
var keyword = obj.options[obj.selectedIndex].value;
var method = document.getElementsByClassName('td_para_'+order)[0];
if(['点击','填写','选择','填写日期','选择全部','验证文字','验证文字非','点击索引'].indexOf(keyword)!= -1){
//    changeBy(keyword,order);
    var methodSelect = method.getElementsByClassName('method');
//        alert(methodSelect.length);
        if(methodSelect.length==0){
               var select = selectOptions(['id','name','class','xpath','text','css'],'id');
                select.setAttribute('onchange','change(this,"'+order+'");');
                select.setAttribute("class","method");
                method.textContent='';
                method.appendChild(select);
        }

}else if(keyword=='公共方法'){
//    changeBy(keyword,order);
    var publicSelect = method.getElementsByClassName('method');
//        alert(methodSelect.length);
        var publicFuntions = getPublicFunctions();
        if(publicSelect.length==0){
               var select = selectOptions(publicFuntions,publicFuntions[0]);
                select.setAttribute('onchange','change(this,"'+order+'");');
                select.setAttribute("class","method");
                method.textContent='';
                method.appendChild(select);
        }
}else{
    var methodSelect = method.getElementsByClassName('method');
    if(methodSelect.length==1){
        method.removeChild(methodSelect[0]);
    }
}
change(obj,order);

}