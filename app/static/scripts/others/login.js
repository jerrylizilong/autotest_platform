$(function(){
    $("body").keydown(function() {
      if (event.keyCode == "13") {//keyCode=13是回车键
            checklogin();
      }
    });
});
//检查登录信息是否正常
function checklogin(){
    var username=$("#username").val();
    var password=$("#password").val();
    $.ajax(
        {
          url: "/checklogin.json",
          data:{"username":username,"password":password},
          type: "get",
          dataType:"json",
          beforeSend:function()
          {
            return true;
          },
          success:function(data)
          {
              if(data["msg"]=='登录成功'){
                window.location.href="/index";

              }
              else{
                $("#msg").html(data["msg"]);
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

function updateButton(){
       $("#new_user").validate({
				submitHandler: function(form) {
				//验证通过后 的js代码写在这里
                    var password=$("#password").val();
                    $.ajax(
                        {
                          url: "/user_password.json",
                          data:{"password":password},
                          type: "get",
                          dataType:"json",
                          beforeSend:function()
                          {
                            return true;
                          },
                          success:function(data)
                          {
                              alert(data["msg"]);

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
	    })

}
