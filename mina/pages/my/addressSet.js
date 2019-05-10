//获取应用实例
var commonCityData = require('../../utils/city.js');
var app = getApp();
Page({
    data: {
        info: [],
        addressList: [],
        selAddress: '请选择',
        index: 0,
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id: e.id
        });
        this.initAddress();
    },
    onShow: function () {
        this.getInfo();
    },
    //初始化地址
    initAddress: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/my/address/all"),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                   addressList:resp.data.list
                });
            }
        });

    },
    bindPickerChange(e) {
        this.setData({
            index: e.detail.value
        })
    },
    bindCancel: function () {
        wx.navigateBack({});
    },
    bindSave: function (e) {
        var that = this;
        var nickname = e.detail.value.nickname;
        var mobile = e.detail.value.mobile;
        var address = that.data.addressList[that.data.index];

        if (nickname == "") {
            app.tip({content: '请填写联系人姓名~~'});
            return
        }
        if (mobile == "") {
            app.tip({content: '请填写手机号码~~'});
            return
        }

        wx.request({
            url: app.buildUrl("/my/address/set"),
            header: app.getRequestHeader(),
            method: "POST",
            data: {
                id: that.data.id,
                address:address,
                nickname: nickname,
                mobile: mobile,
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                // 跳转
                wx.navigateBack({});
            }
        })
    },
    deleteAddress: function (e) {
        var that = this;

        wx.request({
            url: app.buildUrl("/my/address/ops"),
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                id: that.data.id,
                act:'del'
            },
            success: function (res) {
                var resp = res.data;
                app.alert({"content": resp.msg});
                if (resp.code == 200) {
                    // 跳转
                    wx.navigateBack({});
                }
            }
        });
        app.tip(params);
    },
    getInfo: function () {
        var that = this;
        if (that.data.id < 1) {
            return;
        }
        wx.request({
            url: app.buildUrl("/my/address/info"),
            header: app.getRequestHeader(),
            data: {
                id: that.data.id
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                var info = resp.data.info;
                that.setData({
                    info: info,
                    selAddress: info.address ? info.address : "请选择",
                });
            }
        });
    }
});
