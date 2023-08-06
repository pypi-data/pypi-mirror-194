addStyle=(url)=>{
    var s = "<link href='"+url+"' type='text/css' rel='stylesheet'/>";
    document.write(s);
}
addScript=(url)=>{
    var s = "<script src='"+url+"'></script>";
    document.write(s);
}

addSrcs=(urls, addFc)=>{
    for(var index in urls){
        var script = urls[index]
        console.log("file to add: "+script)
        addFc(script)
    }
}
addScripts = (urls)=>{
    addSrcs(urls, addScript)
}
add_style = addStyle;
add_script = addScript;
addStyles = (urls)=>{
    addSrcs(urls, addStyle)
}
