// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "//www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an iframe (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
    console.log('aqui');
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

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    // event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
        console.log('carregando próximo');
        player.loadVideoById('OuSdU8tbcHY');
    }
}
