//获取应用实例
var app = getApp();

Page({
    data: {
        order_num:'',
        orcode: ''
    },
    onShow: function () {
        var that = this;
        this.toPay();
    },
    onLoad: function (e) {
         var that = this;
         app.console(e.order_sn)
        that.setData({
            order_num:e.order_sn
        });
    },
    toPay:function ( e ) {
        var that = this;
        wx.request({
            url: app.buildUrl('/order/pay'),
            header: app.getRequestHeader(),
            method:"POST",
            data: {
                'order_sn' : this.data.order_num
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                    orcode: resp.data.info.orcode
                })
                app.console(that.data.orcode)
            }
        });

    }
    // getOrcode:function () {
    //     var that = this;
    //     var data = {
    //         type:this.data.params.type,
    //         goods:JSON.stringify(this.data.params.goods)
    //     };
    //     wx.request({
    //         url:app.buildUrl('/order/index'),
    //         header:app.getRequestHeader(),
    //         method:'POST',
    //         data:data,
    //         success:function (res) {
    //             var resp = res.data;
    //             if(resp.code!=200){
    //                 app.alert({"content":resp.msg});
    //                 return;
    //             }
    //
    //         }
    //     });
    //}

});
