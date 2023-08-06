[
    //(url前缀, 类, 是否静态类, 初始化参数)
    ("func/", servers.test.Test)
    ("page/", webz.Static, 0, ["page", "pages"])
    ("webz/js/", webz.Static, 0, ["webz/js", "webz.js"])
    ("webz/css/", webz.Static, 0, ["webz/css", "webz.css"])
]