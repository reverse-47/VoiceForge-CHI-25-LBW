currentPage = 0;
//characterLength = 2;
//personalityList = ["cute", "strong"];
//conversationLength = [0, 0];
conversationList = [];

let nameList = [];
let toneList = [];
let CharacterList = [];

function send(inputText, tone) {
    // 为当前请求生成一个唯一的messageId
    const messageId = generateMessageId(currentPage);

    // 显示加载状态
    showLoadingMessage(currentPage, inputText, messageId);

    // 调用getReply获取音频数据
    getReply(inputText, "" , conversationList, tone)
        .then(function (responseData) {
            console.log(responseData);
            // 隐藏加载状态并显示播放按钮
            hideLoadingAndShowPlayButton(currentPage, messageId, "data:audio/wav;base64," + responseData['audio']);
        })
        .catch(function (error) {
            console.error("Error:", error);
            // 处理错误（比如隐藏加载状态并显示错误提示）
            hideLoadingAndShowError(currentPage, messageId);
        });
}

function generateMessageId(page) {
    // 基于当前页面生成一个唯一的messageId，这里假设是页面加上消息的索引
    return `${page}_${new Date().getTime()}`; // 这里可以使用时间戳或其他唯一标识符
}

function init(personality, greeting){
    personalityList[currentPage] = personality;
    conversationList.push({"assistant": greeting}); 
}