// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');
tag.src = "//www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an iframe (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('videotag', {
        height: '433',
        width: '770',
        videoId: 'UFKF5jjsqOY',
        playerVars: {
            autoplay: 1,
            color: 'white',
            fs: 1,
            modestbranding: 1,
            rel: 0,
            showinfo: 0,
            theme: 'light'
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    // event.target.playVideo();
}

var play1 = true;

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED && play1) {
        console.log('carregando próximo');
        player.loadVideoById('OuSdU8tbcHY');
        play1 = false;
    }
}

var Lesson = {
    init: function(defconfigs) {
        Lesson.config = {
        };

        $.extend(Lesson.config, defconfigs);

        $.getJSON('/rest' + window.location.pathname, Lesson.loadData);
    },

    loadData: function(data) {
        console.log(data);
    },

    hashChange: function(event) {
        var state = $.bbq.getState();
        console.log(state);
    }
};

$(function() {
    Lesson.init({'player': player});
    $(window).on('hashchange', Lesson.hashChange);
});