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
        merchants:[],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        processing:false
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
    },
    onShow:function(){
        this.getBannerCat();
        this.getMerchantsList();
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
	 toSearch:function( e ){
	        this.setData({
	            merchants:[],
	            loadingMoreHidden:true
	        });
	        this.getMerchantsList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                    url: "/pages/food/list?member_id=" + e.currentTarget.dataset.id
            });
        }
    },
    getBannerCat:function () {
        var that = this;
        wx.request({
            url:app.buildUrl("/food/index"),
            header:app.getRequestHeader(),
            success:function (res) {
                var resp = res.data;
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({
                    banners: resp.data.banner_list,
                    categories:resp.data.cat_list
                });
            }
        });
    },
    getMerchantsList:function(){
        var that = this;
        if(that.data.processing){
            return;
        }
        that.setData({
            processing: true
        });
        wx.request({
            url:app.buildUrl("/food/merchants"),
            header:app.getRequestHeader(),
            data:{
                mix_kw:that.data.searchInput
            },
            success:function (res) {
                var resp = res.data;
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({
                    merchants: resp.data.list,
                    processing:false
                });
            }
        });
    },
    onReachBottom:function(){
        var that = this;
        setTimeout(function () {
            that.getMerchantsList();
        },500);
    },

});
