;
var food_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;

        $(".wrap_search select[name=status]").change(function(){
            $(".wrap_search").submit();
        });
        $(".wrap_search select[name=cat_id]").change(function(){
            $(".wrap_search").submit();
        });
        $(".wrap_search select[name=member_id]").change(function(){
            $(".wrap_search").submit();
        });
        $(".wrap_search .search").click(function(){
            $(".wrap_search").submit();
        });

        $(".remove").click( function(){
            that.ops( "remove",$(this).attr("data") );
        } );

        $(".recover").click( function(){
            that.ops( "recover",$(this).attr("data") );
        } );

    },
    ops:function( act,id ){
        $.ajax({
            url:common_ops.buildUrl( "/food/ops" ),
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
    food_index_ops.init();
} );