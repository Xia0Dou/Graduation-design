//获取应用实例
var app = getApp();
Page({
    data: {},
    onLoad() {

    },
    onShow() {
        this.getInfo();
    },
    getInfo:function () {
        var that = this;
        wx.request({
            url:app.buildUrl("/member/info"),
            header:app.getRequestHeader(),
            success:function (res) {
                var resp = res.data;
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({
                    user_info:resp.data.info
                });
            }
        });
    },
    changePer:function () {
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
    }
});