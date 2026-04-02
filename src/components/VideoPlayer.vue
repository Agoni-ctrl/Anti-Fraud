<template>
  <div class="video-player-container">
    <div class="video-wrapper" @click="togglePlay">
      <video
        ref="videoRef"
        class="video-element"
        :src="videoUrl"
        @click.stop
        @timeupdate="updateProgress"
        @loadedmetadata="onVideoLoaded"
        @error="onVideoError"
        @waiting="onWaiting"
        @canplay="onCanPlay"
      ></video>
      
      <div v-if="!isPlaying && !isLoading" class="play-overlay">
        <div class="play-button">
          <svg viewBox="0 0 24 24" fill="white" width="60" height="60">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
      </div>

      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner"></div>
      </div>

      <div v-if="hasError" class="error-overlay">
        <div class="error-content">
          <svg viewBox="0 0 24 24" fill="#f44336" width="48" height="48">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
          </svg>
          <p class="error-message">视频加载失败</p>
          <p class="error-detail">{{ errorMessage }}</p>
          <button class="retry-btn" @click.stop="retryLoad">重试</button>
        </div>
      </div>
    </div>

    <div class="video-controls">
      <div class="progress-bar-container" @click="seekVideo">
        <div class="progress-bar">
          <div class="progress-filled" :style="{ width: progress + '%' }"></div>
        </div>
      </div>

      <div class="control-buttons">
        <button class="control-btn" @click="togglePlay" :disabled="hasError">
          <svg v-if="!isPlaying" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
            <path d="M8 5v14l11-7z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
          </svg>
        </button>

        <div class="time-display">
          <span>{{ formatTime(currentTime) }}</span>
          <span>/</span>
          <span>{{ formatTime(duration) }}</span>
        </div>

        <div class="volume-control">
          <button class="control-btn" @click="toggleMute">
            <svg v-if="!isMuted" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
            </svg>
          </button>
          <input
            type="range"
            class="volume-slider"
            v-model="volume"
            min="0"
            max="1"
            step="0.1"
            @input="changeVolume"
          >
        </div>

        <button class="control-btn fullscreen-btn" @click="toggleFullscreen" :disabled="hasError">
          <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
            <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  videoUrl: {
    type: String,
    required: true
  }
})

const videoRef = ref(null)
const isPlaying = ref(false)
const isMuted = ref(false)
const volume = ref(1)
const currentTime = ref(0)
const duration = ref(0)
const progress = ref(0)
const isLoading = ref(false)
const hasError = ref(false)
const errorMessage = ref('')

watch(() => props.videoUrl, () => {
  hasError.value = false
  errorMessage.value = ''
  isPlaying.value = false
  currentTime.value = 0
  progress.value = 0
  if (videoRef.value) {
    videoRef.value.load()
  }
})

const togglePlay = () => {
  if (videoRef.value && !hasError.value) {
    if (isPlaying.value) {
      videoRef.value.pause()
    } else {
      const playPromise = videoRef.value.play()
      if (playPromise !== undefined) {
        playPromise.catch(error => {
          console.error('播放失败:', error)
          errorMessage.value = '播放失败: ' + error.message
          hasError.value = true
        })
      }
    }
  }
}

const toggleMute = () => {
  if (videoRef.value) {
    isMuted.value = !isMuted.value
    videoRef.value.muted = isMuted.value
  }
}

const changeVolume = () => {
  if (videoRef.value) {
    videoRef.value.volume = volume.value
    isMuted.value = volume.value === 0
  }
}

const updateProgress = () => {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
    progress.value = (currentTime.value / duration.value) * 100
  }
}

const seekVideo = (event) => {
  if (videoRef.value) {
    const rect = event.currentTarget.getBoundingClientRect()
    const x = event.clientX - rect.left
    const percentage = x / rect.width
    videoRef.value.currentTime = percentage * duration.value
  }
}

const onVideoLoaded = () => {
  if (videoRef.value) {
    duration.value = videoRef.value.duration
    isLoading.value = false
  }
}

const onVideoError = (event) => {
  console.error('视频加载错误:', event)
  hasError.value = true
  errorMessage.value = '无法加载视频文件，请检查文件路径或格式'
  isLoading.value = false
}

const onWaiting = () => {
  isLoading.value = true
}

const onCanPlay = () => {
  isLoading.value = false
}

const retryLoad = () => {
  hasError.value = false
  errorMessage.value = ''
  isLoading.value = true
  if (videoRef.value) {
    videoRef.value.load()
    videoRef.value.play().then(() => {
      isPlaying.value = true
    }).catch(error => {
      console.error('重试播放失败:', error)
      errorMessage.value = '播放失败: ' + error.message
      hasError.value = true
    })
  }
}

const toggleFullscreen = () => {
  if (videoRef.value) {
    if (videoRef.value.requestFullscreen) {
      videoRef.value.requestFullscreen()
    } else if (videoRef.value.webkitRequestFullscreen) {
      videoRef.value.webkitRequestFullscreen()
    } else if (videoRef.value.mozRequestFullScreen) {
      videoRef.value.mozRequestFullScreen()
    }
  }
}

const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

onMounted(() => {
  if (videoRef.value) {
    videoRef.value.volume = volume.value
    isLoading.value = true
  }
})

onBeforeUnmount(() => {
  if (videoRef.value) {
    videoRef.value.pause()
  }
})
</script>

<style scoped>
.video-player-container {
  width: 100%;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
}

.video-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  background: #000;
}

.video-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: background 0.3s ease;
}

.play-overlay:hover {
  background: rgba(0, 0, 0, 0.4);
}

.play-button {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.play-overlay:hover .play-button {
  transform: scale(1.1);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
}

.error-content {
  text-align: center;
  color: white;
  padding: 30px;
}

.error-message {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 15px 0 10px;
}

.error-detail {
  font-size: 0.9rem;
  color: #ccc;
  margin-bottom: 20px;
}

.retry-btn {
  padding: 10px 24px;
  background: #fff;
  color: #333;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #f0f0f0;
}

.video-controls {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 15px 20px;
}

.progress-bar-container {
  width: 100%;
  cursor: pointer;
  margin-bottom: 12px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
}

.progress-filled {
  height: 100%;
  background: #fff;
  border-radius: 2px;
  transition: width 0.1s linear;
}

.control-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
}

.control-btn {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.control-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.time-display {
  color: #fff;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-left: 10px;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}

.volume-slider {
  width: 80px;
  height: 4px;
  -webkit-appearance: none;
  appearance: none; 
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  outline: none;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  background: #fff;
  border-radius: 50%;
  cursor: pointer;
}

.volume-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  background: #fff;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

.fullscreen-btn {
  margin-left: 10px;
}
</style>