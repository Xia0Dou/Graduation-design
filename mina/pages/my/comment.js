//获取应用实例
var app = getApp();
Page({
    data: {
        "content":"好吃",
        "score":10,
        "order_sn":""
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            order_sn: e.order_sn
        })
    },
    scoreChange:function( e ){
        this.setData({
            "score":e.detail.value
        });
    },
    doComment:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/my/comment/add"),
            header: app.getRequestHeader(),
            method:"POST",
            data:{
                order_sn: that.data.order_sn,
                content:that.data.content,
                score:that.data.score
            },
            success: function (res) {
                var resp = res.data;
                app.alert({"content": resp.msg});
                wx.navigateTo({
                    url: "/pages/my/order_list"
                });
                return;
            }
        });
    }
});