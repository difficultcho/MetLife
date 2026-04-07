const app = getApp()

Page({
  data: {
    products: [],
    loading: true,
    selectedProduct: null,  // 当前点击的商品
    showConfirm: false,     // 确认弹窗
  },

  onLoad() {
    this.fetchProducts()
  },

  // 获取商品列表
  fetchProducts() {
    wx.request({
      url: `${app.globalData.baseUrl}/products`,
      success: (res) => {
        const products = res.data.map(p => ({
          ...p,
          image_url: `${app.globalData.staticUrl}/${p.image}`
        }))
        this.setData({ products, loading: false })
      },
      fail: () => {
        wx.showToast({ title: '加载失败', icon: 'error' })
        this.setData({ loading: false })
      }
    })
  },

  // 点击商品
  onProductTap(e) {
    const product = e.currentTarget.dataset.product
    this.setData({ selectedProduct: product, showConfirm: true })
  },

  // 取消选择
  onCancelConfirm() {
    this.setData({ showConfirm: false, selectedProduct: null })
  },

  // 确认选择 → 获取手机号（需要 button 触发）
  onConfirmSelect() {
    this.setData({ showConfirm: false })
    // 确认后展示授权按钮弹窗
    this.setData({ showAuth: true })
  },

  // 获取手机号回调
  onGetPhoneNumber(e) {
    if (e.detail.errMsg !== 'getPhoneNumber:ok') {
      wx.showToast({ title: '需要授权手机号', icon: 'none' })
      return
    }

    const phoneCode = e.detail.code
    this.setData({ showAuth: false })

    // 获取用户昵称
    wx.getUserProfile({
      desc: '用于记录您的选择',
      success: (profileRes) => {
        this.submitSelection(profileRes.userInfo.nickName, phoneCode)
      },
      fail: () => {
        wx.showToast({ title: '需要授权用户信息', icon: 'none' })
      }
    })
  },

  // 提交选择到后端
  submitSelection(nickname, phoneCode) {
    wx.showLoading({ title: '提交中...' })

    // 先用 phoneCode 换取手机号
    wx.request({
      url: `${app.globalData.baseUrl}/wx/phone`,
      method: 'POST',
      data: { code: phoneCode },
      success: (phoneRes) => {
        if (!phoneRes.data.phone) {
          wx.hideLoading()
          wx.showToast({ title: '获取手机号失败', icon: 'error' })
          return
        }

        // 检查是否已选择过
        wx.request({
          url: `${app.globalData.baseUrl}/selection/${app.globalData.openid}`,
          success: (selRes) => {
            if (selRes.data && selRes.data.id) {
              // 已选择过，询问是否更换
              wx.hideLoading()
              wx.showModal({
                title: '提示',
                content: '您已经选择过商品，是否更换为当前选择？',
                success: (modalRes) => {
                  if (modalRes.confirm) {
                    this.doSubmit(nickname, phoneRes.data.phone)
                  }
                }
              })
            } else {
              this.doSubmit(nickname, phoneRes.data.phone)
            }
          }
        })
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '网络错误', icon: 'error' })
      }
    })
  },

  // 执行提交
  doSubmit(nickname, phone) {
    wx.showLoading({ title: '提交中...' })
    wx.request({
      url: `${app.globalData.baseUrl}/selection`,
      method: 'POST',
      data: {
        openid: app.globalData.openid,
        nickname: nickname,
        phone: phone,
        product_id: this.data.selectedProduct.id
      },
      success: (res) => {
        wx.hideLoading()
        wx.showToast({ title: res.data.message || '提交成功', icon: 'success', duration: 2000 })
        this.setData({ selectedProduct: null })
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '提交失败', icon: 'error' })
      }
    })
  }
})
