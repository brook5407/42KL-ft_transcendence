
// Define global variables or functions
window.audioAssets = {
    homeBGM: new Audio('/static/audio/bgm2.mp3'),
    hitSound: new Audio('/static/audio/hit.mp3'),
    scoreSound: new Audio('/static/audio/score.mp3'),
    bgmSound: new Audio('/static/audio/bgm.mp3'),
	drawSound: new Audio('/static/audio/34 暈 2.mp3'),
	winSound: new Audio('/static/audio/70 歡呼聲 2.mp3'),
	loseSound: new Audio('/static/audio/92 Nooo.mp3'),
	// loseSound: new Audio('/static/audio/34 暈 2.mp3'),
	// playSound: function(sound) {
    //     if (this[sound] instanceof HTMLAudioElement) {
    //         this[sound].play();
    //     } else {
    //         console.error(`Sound ${sound} does not exist`);
    //     }
    // },
};

// Preload the audio files
window.audioAssets.homeBGM.load();
window.audioAssets.hitSound.load();
window.audioAssets.scoreSound.load();
window.audioAssets.bgmSound.load();
window.audioAssets.winSound.load();
window.audioAssets.loseSound.load();
window.audioAssets.drawSound.load();



window.audioAssets.hitSound.addEventListener('canplaythrough', () => {
	console.log('Hit sound preloaded');
});

window.audioAssets.scoreSound.addEventListener('canplaythrough', () => {
	console.log('Score sound preloaded');
});

window.audioAssets.bgmSound.addEventListener('canplaythrough', () => {
	console.log('Background music preloaded');
});

window.audioAssets.loseSound.addEventListener('canplaythrough', () => {
	console.log('loseSound music preloaded');
});

window.audioAssets.winSound.addEventListener('canplaythrough', () => {
	console.log('winSound music preloaded');
});

window.audioAssets.drawSound.addEventListener('canplaythrough', () => {
	console.log('drawSound music preloaded');
});

// Optionally handle errors
window.audioAssets.hitSound.addEventListener('error', () => {
	console.error('Failed to preload hit sound');
	alert('Failed to preload hit sound');
});

window.audioAssets.scoreSound.addEventListener('error', () => {
	console.error('Failed to preload score sound');
	alert('Failed to preload score sound');
});

window.audioAssets.bgmSound.addEventListener('error', () => {
	console.error('Failed to preload background music');
	alert('Failed to preload background music');
});

window.audioAssets.homeBGM.loop = true;
window.audioAssets.homeBGM.play();

window.audioAssets.bgmSound.loop = true;

window.audioAssets.pauseALL = function() {
	if (Array.isArray(this)) {
		this.forEach(audio => {
            if (audio instanceof HTMLAudioElement) {
                audio.pause();
            }
        });
    }
};