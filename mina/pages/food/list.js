//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        member_id:0,
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        processing:false
    },
    onLoad: function (e) {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
        that.setData({
            member_id:e.member_id
        });
    },
    onShow:function(){
        this.getFoodList();
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
    toDetailsTap: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    getFoodList:function (e) {
        var that = this;
        if(that.data.processing){
            return;
        }
        that.setData({
            processing: true
        });
        wx.request({
            url:app.buildUrl("/food/search"),
            header:app.getRequestHeader(),
            data:{
                member_id:that.data.member_id
            },
            success:function (res) {
                var resp = res.data;
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({
                    goods: resp.data.list,
                    processing:false
                });
            }
        });
    },
    onReachBottom:function(){
        var that = this;
        setTimeout(function () {
            that.getFoodList();
        },500);
    },

});
