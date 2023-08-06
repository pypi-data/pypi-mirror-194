# webz
```
简单的web服务器框架，实现的是配置文件的读取和调用，内部调用web.py
demo在demo文件夹中，两种配置方式，分别运行：
python run.py
python runz.py
推荐runz.py的配置方式

为了本人自己使用方便把jquery.js和vue.js放进文件夹了，可以不使用或者替换掉，另外有两脚本文件base.js和utils.js，分装了一些方法:
    json调用:
    $.json(url, data, success=(rst)=>{}, error=(rst)=>{})

    页面跳转（带数据）
        _.jump(url, data)
    新页面通过以下方法获取数据：
        _.data()
    页面回跳:
        _.back(backData=null)
    原页面还是通过_.data()获取初始化时的原数据，也可以通过_.backData()获取回跳时设置的数据

    通过js代码引入js文件库:
        addScript(url)

    vue相关：
    组件:
    component(url, id=null)
    实际是把url对应的页面嵌入当前页面

    页面vue创建：
    newVue({
        data(){return {...}},
        mounted(){...},
        methods:{...}
    })

    不太完善的功能：
    submit调用(未实现回调):
    $.submit(url, maps)
    相关使用参考demo/test.html

    要使用这两个工具类，需要把/webz/js映射成webz.js，并在页面引入脚本:
        <script src="/webz/js/base.js"></script>

任意一个运行后，尝试访问网址：
http://127.0.0.1:8080/page/test.html
http://127.0.0.1:8080/func/abc?d=e&f=g

```
