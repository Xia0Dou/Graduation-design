//获取应用实例
var app = getApp();
Page({
    data: {
        id:0,
        purview : 1,
        list:[]
    },
    onLoad(e) {
        var that =this;
        that.setData({
            purview : that.data.purview,
        });
    },
    onShow() {
        var that = this;
        that.getPur();
        that.getFood();
    },

    getFood:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/merchants/food"),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                   list:resp.data.list
                });
            }
        });
    },
    getPur:function(){
        var that = this;
        wx.request({
            url:app.buildUrl("/member/getPur"),
            header:app.getRequestHeader(),
            success:function (res) {
                var resp = res.data;
                that.setData({
                    purview:resp.data.purview
                });
            }
        });

    },
    changePur:function () {
        var that = this;
        wx.request({
            url:app.buildUrl("/member/change"),
            header:app.getRequestHeader(),
            method:"POST",
            success:function (res) {
                var resp = res.data;
                app.alert({"content":resp.msg});
                that.onShow();
                return;
            }
        });
    },
    toCreate:function () {
        wx.navigateTo({
            url: "/pages/merchants/foodSet?id=0"
        });
    },
    toSet:function (e) {
        wx.navigateTo({
            url: "/pages/merchants/foodSet?id=" + e.currentTarget.dataset.id
        });
    },
    toDelete:function (e) {
        var that = this;
        //发送请求到后台删除数据
        wx.request({
            url:app.buildUrl("/merchants/delete"),
            header:app.getRequestHeader(),
            method:"POST",
            data:{
                id:e.currentTarget.dataset.id
            },
            success:function (res) {
                var resp = res.data;
                app.alert({"content":resp.msg});
                that.getFood();
                return;

            }
        });
    },
    toOrder:function () {
        wx.navigateTo({
            url: "/pages/merchants/merchants_list"
        });
    }
});