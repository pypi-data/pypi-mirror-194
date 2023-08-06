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
        local:"_.local",
        href:"_.href",
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
        _.cache.set(_.key.href, url);
        $('body').load(url);
    },
    jump:(url, data=null, newPage=false)=>{
        console.log("jump:"+url)
        console.log("data:"+data)
        console.log(data)
        if (_.cache.get(_.key.stack) == null){
            _.cache.set(_.key.stack, [])
        }
        var stack = _.cache.get(_.key.stack);
        var href = "";
        if (newPage) {
            href = window.location.href;
        } else {
            href = _.cache.get(_.key.href);
        }
        stack = stack.concat({url:href, data:_.data()});
        _.cache.set(_.key.data, data);
        _.cache.set(_.key.stack, stack)
        if (newPage) {
            window.location.href=url;
        } else {
            _.body(url);
        }
    },
    clean:() => {
        _.cache.set(_.key.stack, []);
    },
    back:(data=null, newPage=false)=>{
        console.log("back:")
        console.log(data)
        var stack = _.cache.get(_.key.stack);
        if (stack.length==0){
            return;
        }
        _.cache.set(_.key.backData, data);
        var obj = stack[stack.length-1]
        var url = obj['url'];
        var cacheData = obj['data']
        stack.pop();
        _.cache.set(_.key.stack, stack);
        _.cache.set(_.key.data, cacheData);
        if (newPage) {
            window.location.href=url;
        } else {
            _.body(url);
        }
        //$('body').load(url);
        //window.location.href=url;
    },
    page: {
        jump: (url, data=null) => {
            _.jump(url, data, true);
        },
        back: (data=null) => {
            _.back(data, true);
        }
    },
    data: () => {
        var _data = _.cache.get(_.key.data)
        //_.cache.set(_.key.data, null)
        if (_data==null){
            _data={};
        }
        return _data;
    },
    backData: () => {
        var _data = _.cache.get(_.key.backData)
        //_.cache.set(_.key.data, null)
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
//addScript("/webz/js/utils_img.js")