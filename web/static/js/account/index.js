;
var account_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        $(".wrap_search .search").click(function(){
            $(".wrap_search").submit();
        });

    },
    ops:function( act,id ){
        $.ajax({
            url:common_ops.buildUrl( "/account/ops" ),
            type:'POST',
            data:{
                act:act,
                id:id
            },
            dataType:'json',
            success:function( res ){
                var callback = null;
                if( res.code == 200 ){
                    callback = function(){
                        window.location.href = window.location.href;
                    }
                }
                common_ops.alert( res.msg,callback );
            }
        });
    }

};

$(document).ready( function(){
    account_index_ops.init();
} );