function getReply(inputText, personality, lastConversation, toneEbd) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/getReply',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({inputText:inputText, personality:personality, lastConversation:lastConversation, toneEbd:toneEbd}),
            success: function (data) {
                resolve(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}

function getGreeting(inputText) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/getGreeting',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({inputText:inputText}),
            success: function (data) {
                resolve(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}