[
    //(url前缀, key, 初始化参数)
    ("func/", test.func)
    ("rest/upload", test.file)
    ("page/", webz.static, ["page", "pages"])
    ("webz/js/", webz.static, ["webz/js", "webz.js"])
    ("webz/css/", webz.static, ["webzcss", "webz.css"])
]