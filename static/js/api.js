function getTextReply(inputText, personality, lastConversation) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/getTextReply',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({inputText:inputText, personality:personality, lastConversation:lastConversation}),
            success: function (data) {
                resolve(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}

function getAudioReply(inputText, fileName) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/getAudioReply',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({inputText:inputText, fileName:fileName}),
            success: function (data) {
                resolve(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}