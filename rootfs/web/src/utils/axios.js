import axios from 'axios'
import { ElMessage } from 'element-plus'

// 环境的切换
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/json'

axios.interceptors.request.use(
    (config)=>{
        let token = sessionStorage.getItem('csrftoken')
        if(token){
            config.headers['X-CSRFToken'] = token;
        }
        return config
    }
)

// 响应拦截器
axios.interceptors.response.use(
    response => {
      // 如果返回的状态码为200，说明接口请求成功，可以正常拿到数据
      // 否则的话抛出错误
      if ([200, 201, 204].indexOf(response.status) >= 0) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(response);
      }
    },
    // 服务器状态码不是2开头的的情况
    // 这里可以跟你们的后台开发人员协商好统一的错误状态码
    // 然后根据返回的状态码进行一些操作，例如登录过期提示，错误提示等等
    // 下面列举几个常见的操作，其他需求可自行扩展
    error => {
      if (error.response.status) {
        console.log('error.request: ', error.request)
        console.log('error.response: ', error.response)
        switch (error.response.status) {
            // 401: 未登录
            // 未登录则跳转登录页面，并携带当前页面的路径
            // 在登录成功后返回当前页面，这一步需要在登录页操作。
          case 401:
            window.location.replace(axios.defaults.baseURL + "/login/drycc/");
            break;
          // 403 无权限
          // 如果获取csrf token失败则表明原有的登陆失效，需要跳转登陆页面。
          // 其他情况正常弹出框显示错误信息即可
          case 403:
            if(error.response.config.url == "/auth/csrf/"){
              window.location.replace(axios.defaults.baseURL + "/login/drycc/");
            } else {
              if(error.response.data){
                ElMessage.error(error.response.data.replace("\"","").replace("\"",""))
              }else {
                  ElMessage.error("You do not have permission to perform this action.")
              }
            }
            break;
          case 404:
            if(error.response.data){
                ElMessage.error(error.response.data.replace("\"","").replace("\"",""))
            }else {
                ElMessage.error("The requested data does not exist.")
            }
            break;
            // 其他错误，直接抛出错误提示
          default:
            console.log({
              message: error.response.data.message,
              duration: 1500,
              forbidClick: true
            });
        }
        return Promise.reject(error.response);
      }
    }
);

export default axios
