currentPage = 1;
characterLength = 2;
personalityList = ["cute", "strong"];
conversationLength = [0, 0];
conversationList = [];

function send(inputText) {
    conversationLength[currentPage]++;
    var length = conversationLength[currentPage];
    showInputMessage(currentPage, inputText, length);
    getTextReply(inputText, personalityList[currentPage], "")
        .then(function (responseData) {
            console.log(responseData);
            showResponseMessage(currentPage, responseData, length);
            getAudioReply(responseData, './static/audio/'+String(currentPage)+String(conversationLength[currentPage])+'.wav')
                .then(function(responseData){
                    console.log(responseData);
                    showAudioBtn(currentPage, length);
                    resolve(); // 执行完成后调用 resolve
                })
                .catch(function (error) {
                    reject(error); // 发生错误时调用 reject
                });
        })
        .catch(function (error) {
            reject(error); // 发生错误时调用 reject
        });
}