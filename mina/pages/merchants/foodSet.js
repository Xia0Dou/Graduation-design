//获取应用实例
var commonCityData = require('../../utils/city.js');
var app = getApp();
Page({
    data: {
        id: 0,
        name: '',
        price: '',
        image: '',
        note: '',
        index:0,
        catList:[]
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id: e.id
        });
        that.getCat();
    },
    onShow: function () {
        this.getInfo();
    },
    getCat:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/merchants/cat"),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                that.setData({
                    catList: resp.data.list
                });
            }
        });
    },
    bindCancel: function () {
        wx.navigateBack({});
    },
    bindPickerChange(e) {
        this.setData({
            index: e.detail.value
        })
    },
    bindSave: function (e) {
        var that = this;
        var name = e.detail.value.name;
        var price = e.detail.value.price;
        var image = e.detail.value.image;
        var note = e.detail.value.note;
        var cat = that.data.catList[that.data.index];

        if (name == "") {
            app.tip({content: '请填写美食名'});
            return
        }
        if (price == "") {
            app.tip({content: '请填写价格'});
            return
        }
        if (image == "") {
            app.tip({content: '请填写图片'});
            return
        }

        wx.request({
            url: app.buildUrl("/merchants/merchants/set"),
            header: app.getRequestHeader(),
            method: "POST",
            data: {
                id: that.data.id,
                cat:cat,
                name: name,
                price: price,
                image: image,
                note: note
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
    getInfo: function () {
        var that = this;
        if (that.data.id < 1) {
            return;
        }
        wx.request({
            url: app.buildUrl("/merchants/food/info"),
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
                });
            }
        });
    }
});
