
const { defineConfig } = require('@vue/cli-service'); // 如果你的项目是这样初始化的

module.exports = defineConfig({ // 或者直接 module.exports = { ... } 如果没有用 defineConfig
  transpileDependencies: true,
  devServer: {
    proxy: {
      // '/api': { // 匹配所有以 /api 开头的请求路径
      //   target: 'http://localhost:5000', // 目标服务器地址
      //   changeOrigin: true, // 对于虚拟主机托管的后端API是必需的，通常建议开启
      //   ws: true, // 如果你的后端API也使用 WebSocket，通常也建议开启，但对普通HTTP请求无影响
      //   // pathRewrite: {'^/api' : ''}, // 只有当你的 Flask API 路径本身不包含 /api 前缀时才需要
      //                                 // 根据你的 Flask @app.route('/api/gis/...'), 你不需要 pathRewrite
      //   // secure: false, // 如果目标服务器是HTTPS且证书无效（开发时），可能需要，但你的是HTTP
      //   // logLevel: 'debug' // <<--- 可以尝试添加这个，看代理是否有更详细的日志输出
      }
    }
})