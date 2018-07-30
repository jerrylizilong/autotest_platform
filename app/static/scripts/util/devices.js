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

