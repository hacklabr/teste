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
        videoId: '',
        playerVars: {
            autoplay: 0,
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
    Lesson.loadReady('player');
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
        console.log('carregando próximo');
        Lesson.videoEnded(event);
    }
}

var Lesson = {
    blocks: undefined,
    state: undefined,
    ready: {player: false,
            data: false},

    init: function(defconfigs) {
        Lesson.config = {
        };

        Lesson.state = $.bbq.getState();
        $.extend(Lesson.config, defconfigs);

        $.getJSON('/rest' + window.location.pathname, Lesson.loadData);
    },

    loadData: function(data) {
        console.log(data);
        Lesson.blocks = data.blocks;
        Lesson.loadReady('data');
    },

    loadReady: function(what) {
        Lesson.ready[what] = true;
        notloaded = $.map(Lesson.ready, function(value, key) {
            return value?null:key;
        });

        if (notloaded.length === 0) {
            Lesson.loadBlock(Lesson.state.blk);
        }
    },

    hashChange: function(event) {
        var state = $.bbq.getState();
        if (Lesson.state.blk != state.blk) {
            Lesson.loadBlock(state.blk);
        }

        Lesson.state = state;
        console.log(state);
    },

    videoEnded: function(event) {
        var position = Lesson.state.blk;
        var next_pos = position + 1;
        if (next_pos >= Lesson.blocks.length) {
            next_pos = 0;
        }
        $.bbq.pushState({'blk': next_pos});
    },

    loadBlock: function(position) {
        var blk = Lesson.blocks[position];
        console.log(blk.video);
        console.log('carregando ' + blk.video.youtube_id);
        player.cueVideoById(blk.video.youtube_id);
    }
};

$(function() {
    Lesson.init({'player': player});
    $(window).on('hashchange', Lesson.hashChange);
});