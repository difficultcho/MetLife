const envConfig = {
  develop: { api: 'http://127.0.0.1:8001/metlife/api', static: 'http://127.0.0.1:8001/metlife/static' },
  trial: { api: 'https://bce.kkmsee.com/metlife/api', static: 'https://bce.kkmsee.com/metlife/static' },
  release: { api: 'https://bce.kkmsee.com/metlife/api', static: 'https://bce.kkmsee.com/metlife/static' },
}
const env = envConfig[__wxConfig.envVersion] || envConfig.release

App({
  globalData: {
    baseUrl: env.api,
    staticUrl: env.static,
    openid: '',
    sessionKey: ''
  },

  onLaunch() {
    this.login()
  },

  login() {
    // 开发环境使用模拟 openid
    if (__wxConfig.envVersion === 'develop') {
      this.globalData.openid = 'dev_test_openid'
      return
    }

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
