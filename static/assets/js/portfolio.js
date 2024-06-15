document.addEventListener('DOMContentLoaded', () => {
  const videos = document.querySelectorAll('.video-hover');

  videos.forEach(video => {
    video.addEventListener('mouseover', () => {
      video.play();
    });

    video.addEventListener('mouseout', () => {
      video.pause();
      video.currentTime = 0;
    });

    video.addEventListener('click', () => {
      video.muted = !video.muted;
      if (video.requestFullscreen) {
        video.requestFullscreen();
      } else if (video.mozRequestFullScreen) {
        video.mozRequestFullScreen();
      } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen();
      } else if (video.msRequestFullscreen) {
        video.msRequestFullscreen();
      }
    });
  });
});
