 function keyOnClick(e){
    var theEvent = window.event || e;
    var code = theEvent.keyCode || theEvent.which;
    if (code==13) {  //回车键的键值为13
            var username=$('#username').val();
            var msg=$('#msg').val();
            if (username==''){
                alert('好友不能为空');
                return;
            }
            if (msg==''){
                alert('信息不能为空');
                return;
            }
            var data= {
                data: JSON.stringify({
                    'username': username,
                    'msg': msg
                }),}
                $.ajax({
                url:'./sendmsg',
                type:'POST',
                data:data,
                dataType: 'json',
               success:function(res){
                    $('#msg').val('');
                    $("#status").html('已发送');

                },
                error:function (res) {
                    console.log(res);
                }

            })
    }
}