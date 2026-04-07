App({
  globalData: {
    baseUrl: 'https://bce.kkmsee.com/metlife/api',
    openid: '',
    sessionKey: ''
  },

  onLaunch() {
    this.login()
  },

  login() {
    wx.login({
      success: (res) => {
        wx.request({
          url: `${this.globalData.baseUrl}/wx/login`,
          method: 'POST',
          data: { code: res.code },
          success: (resp) => {
            if (resp.data.openid) {
              this.globalData.openid = resp.data.openid
              this.globalData.sessionKey = resp.data.session_key
            }
          }
        })
      }
    })
  }
})
