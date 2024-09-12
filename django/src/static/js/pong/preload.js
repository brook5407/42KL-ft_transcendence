// Define global variables or functions
window.audioAssets = {
    hitSound: new Audio('/static/audio/hit.mp3'),
    scoreSound: new Audio('/static/audio/score.mp3')
};

// Preload the audio files
window.audioAssets.hitSound.load();
window.audioAssets.scoreSound.load();

window.audioAssets.hitSound.addEventListener('canplaythrough', () => {
    console.log('Hit sound preloaded');
});

window.audioAssets.scoreSound.addEventListener('canplaythrough', () => {
    console.log('Score sound preloaded');
});

// Optionally handle errors
window.audioAssets.hitSound.addEventListener('error', () => {
    console.error('Failed to preload hit sound');
});

window.audioAssets.scoreSound.addEventListener('error', () => {
    console.error('Failed to preload score sound');
});
