window.alert = alert;

function alert(data) {
    var div = document.createElement("div"),
        h1 = document.createElement('h1'),
        p = document.createElement("p"),
        btn = document.createElement("a"),
        textNode = document.createTextNode(data ? data : ""),
        btnText = document.createTextNode("确 定"),
        h1_text = document.createTextNode('· 温馨提示 ·');
    // 控制样式
    css(div, {
        'background-image': 'url("../static/img/alert_bg.jpg")',
        'background-size': 'cover',
        //'background-position': 'top left',
        'width': '350px',
        'height': '150px',
        'text-align': 'center',
        'background-repeat': 'no-repeat',
        "position": "fixed",
        "left": "30%",
        "top": "20px",
        'font-family': '"Microsoft YaHei", Arial, sans-serif'
        // 'opacity': '0.7'
    });
    css(h1, {
        'padding-top': '25px',
        'font-size': '15px',
        'margin-top': '0',
        'color': '#0c0d10'
    });
    css(p, {
        'color': '#ff16ad',
        'font-size': '12px',
        'font-weight':'700', //字体加粗 100-900
        'padding-top': '10px'
    });
    css(btn, {
        'cursor': 'pointer',
        'width': '50px',
        'height': '25px',
        // 立体效果
        'color': '#0c0d10',
        'background': '#a5cd4e',
        'background': '-moz-linear-gradient(top,  #a5cd4e 0%, #6b8f1a 100%)',
        'background': '-webkit-gradient(linear, left top, left bottom, color-stop(0%,#a5cd4e), color-stop(100%,#6b8f1a))',
        'background': '-webkit-linear-gradient(top,  #a5cd4e 0%,#6b8f1a 100%)',
        'background': '-o-linear-gradient(top,  #a5cd4e 0%,#6b8f1a 100%)',
        'background': '-ms-linear-gradient(top,  #a5cd4e 0%,#6b8f1a 100%)',
        'background': 'linear-gradient(top,  #a5cd4e 0%,#6b8f1a 100%)',
        // 处理圆角
        'display': 'inline-block',
        'position': 'relative',
        'margin': '10px',
        'text-align': 'center',
        'text-decoration': 'none',
        'font': 'bold 12px/25px Arial, sans-serif',
        'text-shadow': '1px 1px 1px rgba(255,255,255, .22)',
        '-webkit-border-radius': '10px',
        '-moz-border-radius': '10px',
        'border-radius': '10px',
        '-webkit-box-shadow': '1px 1px 1px rgba(0,0,0, .29), inset 1px 1px 1px rgba(255,255,255, .44)',
        '-moz-box-shadow': '1px 1px 1px rgba(0,0,0, .29), inset 1px 1px 1px rgba(255,255,255, .44)',
        'box-shadow': '1px 1px 1px rgba(0,0,0, .29), inset 1px 1px 1px rgba(255,255,255, .44)',
        '-webkit-transition': 'all 0.15s ease',
        '-moz-transition': 'all 0.15s ease',
        '-o-transition': 'all 0.15s ease',
        '-ms-transition': 'all 0.15s ease',
        'transition': 'all 0.15s ease'
    });
    // 内部结构套入
    h1.appendChild(h1_text);
    p.appendChild(textNode);
    btn.appendChild(btnText);
    div.appendChild(h1);
    div.appendChild(p);
    div.appendChild(btn);
    // 整体显示到页面内
    document.getElementsByTagName("body")[0].appendChild(div);
    // 确定绑定点击事件删除标签
    btn.onclick = function () {
        div.parentNode.removeChild(div);
    };
    setTimeout(function () {
        div.parentNode.removeChild(div);
    },3000);
}

function css(targetObj, cssObj) {
    var str = targetObj.getAttribute("style") ? targetObj.getAttribute("style") : "";
    for (var i in cssObj) {
        str += i + ":" + cssObj[i] + ";";
    }
    targetObj.style.cssText = str;
}