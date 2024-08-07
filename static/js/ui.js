function create_element({
    type = 'div', 
    textContent = undefined, 
    src = undefined,
    id = undefined, 
    className = undefined, 
    onclick = undefined,
}) {
    var newdiv = document.createElement(type);
    if (textContent !== undefined)
        newdiv.textContent = textContent;
    if (src !== undefined)
        newdiv.src = src;
    if (id !== undefined)
        newdiv.id = id;
    if (className !== undefined)
        newdiv.className = className;
    if (onclick !== undefined)
        newdiv.onclick = onclick;
    return newdiv;
}

function changePage(id)
{
    for(var i=0; i<characterLength;i++)
    {
        document.getElementById("character"+String(i)).className = "character_box";
    }
    document.getElementById("character"+String(id)).className = "character_box_selected";
}

function showInputMessage(currentPage, content, length) {
    var message = create_element({className: 'message'});
    var div = create_element({
        textContent: content, 
        className: 'input_text',
        id: String(currentPage)+'input'+String(length)
    });
    message.appendChild(div);
    document.getElementById("content"+String(currentPage)).appendChild(message);
}

function showResponseMessage(currentPage, content, length) {
    var message = create_element({className: 'message'});
    var div = create_element({
        textContent: content, 
        className: 'response_text',
        id: String(currentPage)+'response'+String(length)
    });
    var btn = create_element({
        type:'img',
        src: '/static/img/speek.png',
        className: 'audio_btn',
        id: String(currentPage)+'audio'+String(length)
    });
    var load = create_element({
        type:'img',
        src: '/static/img/loading.gif',
        className: 'load_btn',
        id: String(currentPage)+'loading'+String(length)
    });
    btn.style.display = "none";
    message.appendChild(div);
    message.appendChild(load);
    message.appendChild(btn);
    document.getElementById("content"+String(currentPage)).appendChild(message);
}

function showAudioBtn(currentPage, length){
    document.getElementById(String(currentPage)+'loading'+String(length)).style.display = "none";
    document.getElementById(String(currentPage)+'audio'+String(length)).style.display = "block";
    let audio = new Audio('/static/audio/'+String(currentPage)+String(length)+'.wav');
    document.getElementById(String(currentPage)+'audio'+String(length)).onclick = function() {
        audio.play();
    };
}