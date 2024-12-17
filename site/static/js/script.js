document.getElementById('start-btn').addEventListener('click', () => {
    document.getElementById('video-feed').src = "/video_feed";
});

document.getElementById('stop-btn').addEventListener('click', async () => {
    document.getElementById('video-feed').src = "";
    await fetch('/stop_camera', { method: 'POST' });
});
