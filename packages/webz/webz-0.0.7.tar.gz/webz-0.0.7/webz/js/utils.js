$.count = 0;
function sleep(ms) {    
    return new Promise(resolve => setTimeout(resolve, ms));
}
repeat=(ms, fc)=>{
    setInterval(fc, ms);
}
async function test() {
    while($.count>0){
        await sleep(100);
    }
}

newVue=async (args)=>{
    await sleep(1);
    while($.count>0){
        await sleep(100);
    }
    if (!args.el) {
        args.el="#app"
    }
    var vue=new Vue(args)
    _.vue = vue
    return vue;
}

$.jump=function(url){
    //window.location.href=url;
    $('body').load(url);
}

function sleepx(ms){
    var t = Date.now();
    while(Date.now() - t <= ms);
}
$.component=(url, id=null)=>{
    $.count+=1;
    if(id == null){
        arr = url.split("/")
        id = arr[arr.length-1]
        id = id.split(".")[0]
    }
    var key = "#"+id;
    $.get(url,(rst)=>{
        var items = $(rst);
        items.appendTo(document.body);
        $.count-=1;
        return;
    })
    return this;
}
let component = $.component;

$.upload=(url, data, success, error= (msg)=>{
    console.log("error in $.upload");
    console.log(msg);
    console.log(msg.responseText)
    }
)=>{
    var form = new FormData();
    for (var k in data) {
        form.append(k, data[k]);
    }
    $.ajax({
        type: "POST",
        url: url,
        data: form,
        contentType: false,
        processData: false,
        success: success,
        error: error
    })
}
$.submit=(url, data, success, error= (msg)=>{
    console.log("error in $.submit");
    console.log(msg);
    console.log(msg.responseText)
    }
)=>{
    var form = new FormData();
    for (var k in data) {
        form.append(k, data[k]);
    }
    $.ajax({
        type: "POST",
        url: url,
        data: form,
        contentType: false,
        processData: false,
        success: success,
        error: error
    })
}

$.submit_bk=function(url, maps){
    var body=$(document.body);
    var form = $("<form method='post'></form>");
    var input;
    form.attr({"action":url})
    $.each(maps, (key, value)=>{
        input = $("<input type='hodden'>");
        input.attr({"name":key});
        input.val(value)
        form.append(input)
    });
    form.appendTo(document.body);
    form.submit();
    document.body.removeChild(form[0]);
}

$.json=(url, data, success, error= (msg)=>{
    console.log("error in $.json");
    console.log(msg);
    console.log(msg.responseText)
    }
)=>{
    data= JSON.stringify(data);
    $.ajax({
        type:"POST",
        url:url,
        contentType:"application/json;charaset=utf-8",
        data:data,
        dataType:"json",
        success:success,
        error:error
    })
}
//document.addEventListener('readystatechange', () => console.log(document.readyState))

let _={
    sleep:(ms)=>{
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    cache:{
        set(key,val){
            var s = _.jd(val)
            //console.log("[LOG] _.cache.set('"+key+"'):["+s+"]")
            window.localStorage[key]=s;
        },
        get(key){
            var val = window.localStorage[key];
            //console.log("[LOG] _.cache.get('"+key+"'):["+val+"]:"+typeof(val))
            if (val==null){
                return val;
            }
            var obj=null;
            try{
                obj = _.jl(val);
            }catch(err){
                console.log("[LOG] Error in _.jsonloads:")
                console.log(err)
            }
            //console.log("[LOG] _.jl:")
            //console.log(obj)
            return obj;
        }
    },
    key:{
        data:"_.data",
        stack:"_.stack",
        forward:"_.forward",
        local:"_.local",
        href:"_.href",
        count:"_.count",
        refresh: "_.refresh",
        backData: "_.backData"
    },
    cleanCache(){
        for(var k in _.key){
            var key = _.key[k];
            _.cache.set(key, null)
        }
    },
    jsonloads(s){
        return $.parseJSON(s);
    },
    jsondumps(obj){
        return JSON.stringify(obj);
    },
    jl(s){
        return $.parseJSON(s);
    },
    jd(obj){
        return JSON.stringify(obj);
    },
    body: (url) => {
        _.singlePage()
        _.history.href.set(url)
        $('body').load(url);
    },
    history: {
        get:(key) => {
            var data = _._history[key];
            if (_.newPage||_.useCache) {
                data = _.cache.get(_.key[key])
            }
            if (data == null) {
                return data;
            }
            return _.jl(data);
        },
        set:(key, data) => {
            data = _.jd(data);
            if (_.newPage||_.useCache) {
                _.cache.set(_.key[key], data)
            } else {
                _._history[key] = data;
            }
        },
        size:(key) => {
            var stack = _._history[key];
            if (_.newPage||_.useCache) {
                stack = _.cache.get(_.key[key])
            }
            if (stack == null) {
                stack = [];
            }
            return stack.length
        },
        push:(key, url, data)=>{
            var stack = _._history[key];
            if (_.newPage||_.useCache) {
                stack = _.cache.get(_.key[key])
            }
            if (stack == null) {
                stack = [];
            }
            data = _.jd(data);
            stack = stack.concat({url:url, data:data})
            if (_.newPage||_.useCache) {
                _.cache.set(_.key[key], stack)
            } else {
                _._history[key] = stack;
            }
        },
        pop:(key)=>{
            var stack = _._history[key];
            if (_.newPage||_.useCache) {
                stack = _.cache.get(_.key[key])
            }
            if (stack == null) {
                stack = [];
            }
            if (stack.length==0) {
                return null;
            }
            var data = stack[stack.length-1]
            data['data'] = _.jl(data['data'])
            stack.pop();
            if (_.newPage||_.useCache) {
                _.cache.set(_.key[key], stack)
            } else {
                _._history[key] = stack;
            }
            return data
        },
        clean:(key)=>{
            if (_.newPage||_.useCache) {
                _.cache.set(_.key[key], []);
            } else {
                _._history[key] = [];
            }
        },
        stack: {
            push:(url, data) =>{return _.history.push("stack", url, data)},
            pop:() => {return _.history.pop("stack")},
            size:()=>{return _.history.size("stack")},
            clean:()=>{return _.history.clean("stack")}
        },
        forward: {
            push:(url, data) =>{return _.history.push("forward", url, data)},
            pop:() => {return _.history.pop("forward")},
            size:()=>{return _.history.size("forward")},
            clean:()=>{return _.history.clean("forward")}
        },
        data: {get:()=>{return _.history.get("data")}, set:(val)=>{_.history.set("data", val)}},
        backData: {get:()=>{return _.history.get("backData")}, set:(val)=>{_.history.set("backData", val)}},
        count: {get:()=>{return _.history.get("count")}, set:(val)=>{_.history.set("count", val)}},
        href: {
            get:()=>{
                if (_.newPage) {
                    return window.location.href;
                } else {
                    return _.history.get("href");
                }
            },
            set:(url) => {
                if (_.newPage) {
                    window.location.href = url
                } else {
                    _.history.set("href", url)
                }
            }
        },
    },
    _history: {
        stack: [],
        forward: [],
        href: "",
        data: null,
        backData: null,
        count: null
    },
    newPage: true,
    useCache: false,
    cacheInHistory(used=true) {
        _.useCache = used;
    },
    singlePage:()=>{
        if (!_.newPage) {
            return;
        }
        console.log("set single");
        _.newPage = false;
        pushHistory(1);
    },
    jump:(url, data=null)=>{
        _.history.forward.clean()
        _.history.stack.push(_.history.href.get(), _.history.data.get())
        _.history.data.set(data);
        history_forward();
        if (_.newPage) {
            window.location.href=url;
        } else {
            _.body(url);
        }
    },
    clean:() => {
        _.history.stack.clean()
        _.history.forward.clean()
        _.history.data.set(null)
        _.history.backData.set(null)
        _.history.count.set(null)
    },
    _forward:() => {
        if (_.history.forward.size()==0) {
            return;
        }
        var obj = _.history.forward.pop()
        var data = _.history.data.get()
        var href = _.history.href.get()
        _.history.stack.push(href, data)
        _.history.data.set(obj['data'])
        if (_.newPage) {
            window.location.href=obj['url'];
        } else {
            _.body(obj['url'])
        }
    },
    back:(data=null)=>{
        _.history.backData.set(data);
        history_back()
    },
    _back:()=>{
        if (_.history.stack.size()==0) {
            return;
        }
        var obj = _.history.stack.pop();
        var url = obj['url'];
        var cacheData = obj['data']
        var href = _.history.href.get()
        var data = _.history.data.get()
        _.history.forward.push(href, data)
        _.history.data.set(cacheData)
        if (_.newPage) {
            window.location.href=url;
        } else {
            _.body(url);
        }
    },
    data: () => {
        var _data = _.history.data.get()
        if (_data==null){
            _data={};
        }
        return _data;
    },
    backData: () => {
        var _data = _.history.backData.get()
        if (_data==null){
            _data={};
        }
        return _data;
    },
    local:{
        clean(){
            _.cache.set(_.key.local, {})
        },
        save:(key, val)=>{
            if( _.cache.get(_.key.local)==null){
                _.cache.set(_.key.local, {})
            }
            var dict = _.cache.get(_.key.local)
            dict[key] = val;
            _.cache.set(_.key.local, dict)
        },
        load:(key)=>{
            if( _.cache.get(_.key.local)==null){
                _.cache.set(_.key.local, {})
            }
            var dict = _.cache.get(_.key.local)
            return dict[key]
        }
    },
    submit:function(url, maps){
        var body=$(document.body);
        var form = $("<form method='post'></form>");
        var input;
        form.attr({"action":url})
        $.each(maps, (key, value)=>{
            input = $("<input type='hodden'>");
            input.attr({"name":key});
            input.val(value)
            form.append(input)
        });
        form.appendTo(document.body);
        form.submit();
        document.body.removeChild(form[0]);
    },
    copy(text){
        var input = document.createElement('input');
        input.value = text;
        document.body.appendChild(input);
        input.select();
        document.execCommand("Copy");
        document.body.removeChild(input);
    },
    $:(obj)=>{
        if (obj.name!=null){
            obj = $(obj)
        }
        return obj;
    }
}
window.onload=()=>{
    console.log("window.onload");
}
function history_forward() {
    var state = history.state;
    var count = 0;
    if (state) {
        count = state.count+1;
    }
    _.history.count.set(count)
    pushHistory(count)
}
function history_back() {
    window.history.back();
}
function pushHistory(cnt) {
    var state = {
        count: cnt
    }; 
    window.history.pushState(state, "title", ""); 
}
function replaceHistory(cnt) {
    var state = {
        count: cnt
    }; 
    window.history.replaceState(state, "title", ""); 
}

window.addEventListener("popstate", function(e) {
    var cacheCount = _.history.count.get();
    if (!e.state || (cacheCount && cacheCount > e.state.count)) {
        console.log("_back")
        _._back();
    } else if (!cacheCount||cacheCount < e.state.count) {
        console.log("_forward")
        _._forward();
    } else {
        console.log("error cache:"+cacheCount+":"+e.state.count)
    }
    if (e.state) {
        _.history.count.set(e.state.count)
    }
}, false);