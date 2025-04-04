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

function getMix(timbreList) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/getMix',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({timbreList: timbreList}),
            success: function (data) {
                resolve(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}

function getNarrativeAudio(inputText, toneList) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: '/getNarrativeAudio',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({inputText:inputText, toneList: toneList}),
            success: function (data) {
                resolve(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                reject(errorThrown);
            }
        });
    });
}