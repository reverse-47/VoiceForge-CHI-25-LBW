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

function changePage(index) {
    // 获取所有的 content 页面
    currentPage = index;
    var contentList = document.querySelectorAll("#contentList .content");

    // 遍历所有的 content 页面，隐藏不需要的
    contentList.forEach(function(content, idx) {
        if (content.id === "content"+String(index)) {
            content.style.display = "block";  // 显示对应的 content 页面
            document.getElementById("name").textContent = nameList[index];
        } else {
            content.style.display = "none";   // 隐藏其他页面
        }
    });

    // 获取所有的 character-box
    var characterBoxes = document.querySelectorAll("#characterlist .character-box");

    // 遍历所有的 character-box，移除 'character-box-selected' 样式
    characterBoxes.forEach(function(box) {
        box.style.pointerEvents = 'auto';
        box.classList.remove("character-box-selected");
    });

    // 为当前选中的 character-box 添加 'character-box-selected' 样式
    var selectedBox = document.getElementById("character" + index);
    selectedBox.classList.add("character-box-selected");
}

function showInputMessage(currentPage, content, length) {
    var message = create_element({className: 'message'});
    var div = create_element({
        textContent: content, 
        className: 'input-text',
        id: String(currentPage)+'input'+String(length)
    });
    message.appendChild(div);
    document.getElementById("content"+String(currentPage)).appendChild(message);
}

function showResponseMessage(currentPage, content, src) {
    var message = create_element({className: 'message'});
    var div = create_element({
        textContent: content, 
        className: 'response-text',
        // id: String(currentPage)+'response'+String(length)
    });
    var btn = create_element({
        type:'img',
        src: '/static/img/speek.png',
        className: 'audio-btn',
        // id: String(currentPage)+'audio'+String(length)
    });
    btn.onclick = function() {
        var audioPlayer = document.getElementById("audioPlayer");
        if (audioPlayer && typeof src !== 'undefined') {
            audioPlayer.src = src;
            audioPlayer.load(); // 确保新的src被加载
            audioPlayer.play().catch(function(error) {
                console.log("播放失败: ", error);
            });
        } else {
            console.log("音频播放器不存在或src未定义");
        }
    }
    // var load = create_element({
    //     type:'img',
    //     src: '/static/img/loading.gif',
    //     className: 'load-btn',
    //     id: String(currentPage)+'loading'+String(length)
    // });
    // btn.style.display = "none";
    message.appendChild(div);
    // message.appendChild(load);
    message.appendChild(btn);
    document.getElementById("content"+String(currentPage)).appendChild(message);
}

// function showAudioBtn(currentPage, length){
//     document.getElementById(String(currentPage)+'loading'+String(length)).style.display = "none";
//     document.getElementById(String(currentPage)+'audio'+String(length)).style.display = "block";
//     let audio = new Audio('/static/audio/'+String(currentPage)+String(length)+'.wav');
//     document.getElementById(String(currentPage)+'audio'+String(length)).onclick = function() {
//         audio.play();
//     };
// }

function showLoadingMessage(currentPage, content, messageId) {
    var message = create_element({ className: 'message', id: messageId });
    var div = create_element({
        textContent: content,
        className: 'response-text',
    });
    
    // 创建加载图标
    var load = create_element({
        type: 'img',
        src: '/static/img/loading.gif', // 假设这是加载图标的路径
        className: 'load-btn',
    });

    message.appendChild(div);
    message.appendChild(load);

    // 将消息添加到页面
    document.getElementById("content" + String(currentPage)).appendChild(message);
}

function hideLoadingAndShowPlayButton(currentPage, messageId, src) {
    // 找到对应的消息容器
    var messageContainer = document.getElementById(messageId);
    
    if (messageContainer) {
        // 移除加载图标
        var loadIcon = messageContainer.querySelector('.load-btn');
        if (loadIcon) {
            loadIcon.style.display = "none"; // 隐藏加载图标
        }
        
        // 显示播放按钮
        var btn = create_element({
            type: 'img',
            src: '/static/img/speek.png', // 播放按钮图标路径
            className: 'audio-btn',
        });
        
        btn.onclick = function () {
            var audioPlayer = document.getElementById("audioPlayer");
            if (audioPlayer && typeof src !== 'undefined') {
                audioPlayer.src = src;
                audioPlayer.load(); // 确保新的src被加载
                audioPlayer.play().catch(function (error) {
                    console.log("播放失败: ", error);
                });
            } else {
                console.log("音频播放器不存在或src未定义");
            }
        };
        
        messageContainer.appendChild(btn);
    }
}

function hideLoadingAndShowError(currentPage, messageId) {
    // 找到对应的消息容器
    var messageContainer = document.getElementById(messageId);

    if (messageContainer) {
        // 移除加载图标
        var loadIcon = messageContainer.querySelector('.load-btn');
        if (loadIcon) {
            loadIcon.style.display = "none"; // 隐藏加载图标
        }

        // 显示错误提示
        var errorText = create_element({
            textContent: "获取音频失败，请重试。",
            className: 'error-text',
        });

        messageContainer.appendChild(errorText);
    }
}

function activateWrite(index) {
    // 找到对应的按钮和input框
    var characterBox = document.getElementById("character" + index);
    var inputBox = characterBox.querySelector(".name-input");
    var writeIcon = characterBox.querySelector(".write-icon");
    var saveIcon = characterBox.querySelector(".save-icon");

    // 使输入框可编辑
    inputBox.disabled = false;
    
    // 隐藏写入按钮，显示保存按钮
    writeIcon.style.display = "none";
    saveIcon.style.display = "inline-block";
}

function saveName(index) {
    // 找到对应的按钮和input框
    var characterBox = document.getElementById("character" + index);
    var inputBox = characterBox.querySelector(".name-input");
    var writeIcon = characterBox.querySelector(".write-icon");
    var saveIcon = characterBox.querySelector(".save-icon");

    // 更新 nameList 数组
    nameList[index] = inputBox.value;

    // 禁用输入框，显示写入按钮，隐藏保存按钮
    inputBox.disabled = true;
    writeIcon.style.display = "inline-block";
    saveIcon.style.display = "none";

    // 更新 UI 上的显示名称
    characterBox.querySelector(".name-input").value = nameList[index];
}

function addCharacter(name, tone) {
    // 向 NameList 添加一个新的角色
    nameList.push(name);
    toneList.push(tone);
    
    // 向 CharacterList 添加一个新的角色
    var newIndex = CharacterList.length;
    CharacterList.push("character" + newIndex);

    // 在页面中添加新的 character-box
    var characterListDiv = document.getElementById("characterlist");
    var newCharacterBox = document.createElement("button");
    newCharacterBox.className = "character-box";
    newCharacterBox.id = "character" + newIndex;
    newCharacterBox.onclick = function() { changePage(newIndex); };

    var inputBox = document.createElement("input");
    inputBox.className = "name-input";
    inputBox.value = name; // 默认值为 Test
    inputBox.disabled = true;

    var writeIcon = document.createElement("img");
    writeIcon.className = "write-icon";
    writeIcon.src = "/static/img/write.png";
    writeIcon.onclick = function() { activateWrite(newIndex); };

    var saveIcon = document.createElement("img");
    saveIcon.className = "save-icon";
    saveIcon.src = "/static/img/save.png";
    saveIcon.style.display = "none";
    saveIcon.onclick = function() { saveName(newIndex); };

    var deleteIcon = document.createElement("img");
    deleteIcon.className = "delete-icon";
    deleteIcon.src = "/static/img/delete.png";
    deleteIcon.onclick = function() { deleteCharacter(newIndex); };

    newCharacterBox.appendChild(inputBox);
    newCharacterBox.appendChild(writeIcon);
    newCharacterBox.appendChild(saveIcon);
    newCharacterBox.appendChild(deleteIcon);

    characterListDiv.appendChild(newCharacterBox);

    // 创建新的 content 页面
    var contentListDiv = document.getElementById("contentList");
    var newContentDiv = document.createElement("div");
    newContentDiv.className = "content";
    newContentDiv.id = "content" + newIndex;
    newContentDiv.style.display = "none";  // 默认隐藏

    contentListDiv.appendChild(newContentDiv);
    
    // 默认选中刚创建的角色
    changePage(newIndex);
}

function deleteCharacter(index) {
    // 从 NameList 和 CharacterList 中删除对应项
    NameList[index] = "";
     //CharacterList.splice(index, 1);

    // 删除对应的 character-box
    var characterBox = document.getElementById("character" + index);
    characterBox.remove();

    // 删除对应的 content 页面
    var contentBox = document.getElementById("content" + index);
    contentBox.remove();

    // 更新剩余的 character-box 和 content 页面 的 id，以保证顺序正确
    

    // 更新剩余的 content 页面 的 id
    

    // 如果删除的是当前页面，切换到第一个页面
}