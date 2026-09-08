const seamlessVideos = document.querySelectorAll('video');

seamlessVideos.forEach((video) => {
    video.addEventListener('loadedmetadata', () => {
        video.play().catch(() => {});
    });

    video.addEventListener('timeupdate', () => {
        if (video.duration && video.currentTime > video.duration - 0.08) {
            video.currentTime = 0;
            video.play().catch(() => {});
        }
    });
});
