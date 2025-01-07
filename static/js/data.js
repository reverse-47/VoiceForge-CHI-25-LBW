currentPage = 0;
characterLength = 1;
personalityList = ["cute", "strong"];
conversationLength = [0, 0];
conversationList = [];

function send(inputText, tone) {
    conversationLength[currentPage]++;
    var length = conversationLength[currentPage];
    //showInputMessage(currentPage, inputText, length);
    getReply(inputText, personalityList[currentPage], conversationList, tone)
        .then(function (responseData) {
            console.log(responseData);
            showResponseMessage(currentPage, responseData["text"], "data:audio/wav;base64," + responseData['audio'])
            conversationList.push({"user": inputText});
            conversationList.push({"assistant": responseData["text"]});
        })
        .catch(function (error) {
            reject(error); // 发生错误时调用 reject
        });
}

function init(personality, greeting){
    personalityList[currentPage] = personality;
    conversationList.push({"assistant": greeting}); 
}