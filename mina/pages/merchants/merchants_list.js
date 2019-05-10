var app = getApp();
Page({
    data: {
        statusType: ["待支付", "待确认", "待评价", "已完成", "已取消"],
        status:[ "2","3","1","0","4"],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""],
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType
        });
        this.onShow();
    },
        onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;
        that.getPayOrder();
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },
    getPayOrder:function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/merchants/order'),
            header: app.getRequestHeader(),
            data: {
                status:that.data.status[that.data.currentType]
            },
            success: function (res) {
                wx.hideLoading();
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                    order_list: resp.data.pay_order_list
                })

            }
        });
    },
    orderCancel:function (e) {
        var that = this;
        wx.request({
            url: app.buildUrl('/order/cancel'),
            header: app.getRequestHeader(),
            method:"POST",
            data: {
                order_sn:e.currentTarget.dataset.id
            },
            success: function (res) {
                var resp = res.data;
                app.alert({"content": resp.msg});
                if (resp.code == 200) {
                    that.getPayOrder();
                    return;
                }
            }
        });
    },
    orderConfirm:function (e) {
        var that = this;
        wx.request({
            url: app.buildUrl('/merchants/confirm'),
            header: app.getRequestHeader(),
            method:"POST",
            data: {
                order_sn:e.currentTarget.dataset.id
            },
            success: function (res) {
                var resp = res.data;
                app.alert({"content": resp.msg});
                if (resp.code == 200) {
                    that.getPayOrder();
                    return;
                }
            }
        });
    }
})
