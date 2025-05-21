<template>
  <div class="feng-clock-widget">
    <div class="time-and-visuals">
      <div class="time-section">
        <div class="time-display">{{ currentTime }}</div>
        <div class="date-display">{{ currentDateString }}</div>
      </div>
      <div
        class="globe-visual-container"
        @mouseenter="handleGlobeHover(true)"
        @mouseleave="handleGlobeHover(false)"
      >
        <Vue3Lottie
          v-if="globeLottieJson"
          ref="lottiePlayer" :animationData="globeLottieJson"
          :loop="true"
          :autoPlay="true"
          :speed="1" :width="lottieSize.width"
          :height="lottieSize.height"
        />
        <div v-else class="lottie-loading">动画加载中...</div>
      </div>
    </div>
  </div>
</template>

<script>
// 假设 Vue3Lottie 已经在 main.js 全局注册
// import Vue3Lottie from 'vue3-lottie';

import globeAnimationData from '@/assets/lottie/globe-animation.json'; // 确保路径正确

export default {
  name: 'ClockWidget',
  // components: { Vue3Lottie }, // 如果全局注册了，这里不需要
  data() {
    return {
      currentTime: this.formatTime(new Date()),
      currentDate: new Date(),
      timerId: null,
      globeLottieJson: null,
      lottieSize: { width: '75px', height: '75px' }
    };
  },
  computed: {
    currentDateString() {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return this.currentDate.toLocaleDateString('zh-CN', options) + ' ' + this.getDayOfWeek(this.currentDate);
    }
  },
  methods: {
    formatTime(date) {
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');
      return `${hours}:${minutes}:${seconds}`;
    },
    getDayOfWeek(date) {
      return new Intl.DateTimeFormat('zh-CN', { weekday: 'long' }).format(date);
    },
    updateClock() {
      const now = new Date();
      this.currentTime = this.formatTime(now);
      this.currentDate = now;
    },
    handleGlobeHover(isHovering) {
      const player = this.$refs.lottiePlayer;

      if (!player) {
        // console.warn("[ClockWidget] Lottie player ref ('lottiePlayer') not found on hover event.");
        return;
      }

      let actionablePlayPauseInstance = null;
      if (typeof player.play === 'function' && typeof player.pause === 'function') {
        actionablePlayPauseInstance = player;
      } else if (player.animation && typeof player.animation.play === 'function' && typeof player.animation.pause === 'function') {
        actionablePlayPauseInstance = player.animation;
      } else if (typeof player.getLottie === 'function') {
        const lwInstance = player.getLottie();
        if (lwInstance && typeof lwInstance.play === 'function' && typeof lwInstance.pause === 'function') {
          actionablePlayPauseInstance = lwInstance;
        }
      }

      if (actionablePlayPauseInstance) {
        if (isHovering) {
          actionablePlayPauseInstance.pause();
          // console.log("[ClockWidget] Lottie paused.");
        } else {
          actionablePlayPauseInstance.play();
          // console.log("[ClockWidget] Lottie playing.");
        }
      } else {
        // console.warn("[ClockWidget] Suitable play/pause methods were not identified on the Lottie player instance.");
      }
    },
    loadLottieAnimation() {
      if (globeAnimationData) {
        this.globeLottieJson = globeAnimationData;
        // console.log("[ClockWidget] Lottie animation data loaded.");
      } else {
        console.error("[ClockWidget] Failed to load Lottie animation data. Check import path.");
      }
    }
  },
  mounted() {
    this.loadLottieAnimation();
    this.updateClock();
    this.timerId = setInterval(this.updateClock, 1000);

    // LottiePlayer 的 autoPlay=true prop 应该会处理初始播放。
    // 之前在这里的 $nextTick 和手动播放逻辑（引入了未使用的 lottieInstance）已移除，
    // 因为它主要是为了调试 autoPlay 不生效的情况。
    // console.log("[ClockWidget] Mounted hook finished.");
  },
  beforeUnmount() {
    if (this.timerId) {
      clearInterval(this.timerId);
    }
    const player = this.$refs.lottiePlayer;

    if (!player) {
      return;
    }

    let actionableStopInstance = null;
    if (typeof player.stop === 'function') {
        actionableStopInstance = player;
    } else if (player.animation && typeof player.animation.stop === 'function') {
        actionableStopInstance = player.animation;
    } else if (typeof player.getLottie === 'function') {
        const lwInstance = player.getLottie();
        if (lwInstance && typeof lwInstance.stop === 'function') {
            actionableStopInstance = lwInstance;
        }
    }

    if (actionableStopInstance) {
        actionableStopInstance.stop();
        // console.log("[ClockWidget] Lottie stopped on unmount.");
    }
  }
}
</script>

<style scoped>
.feng-clock-widget {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(170, 200, 255, 0.35);
  /* backdrop-filter: blur(10px); */ /* 如果编译有问题，保持注释 */
  border-radius: 14px;
  padding: 15px 20px;
  min-width: 230px;
  width: fit-content;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  color: #FFFFFF;
}

.time-and-visuals {
  display: flex;
  align-items: center;
  gap: 15px;
}

.time-section {
  text-align: right;
}

.time-display {
  font-family: 'Inter', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  font-size: 3.2em;
  font-weight: 600;
  color: #FFFFFF;
  line-height: 1.1;
  margin-bottom: 8px;
  text-shadow: 0px 1px 3px rgba(0, 0, 0, 0.6),
               0px 0px 8px rgba(0, 0, 0, 0.4);
}

.date-display {
  font-family: 'Inter', 'Noto Sans SC', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  font-size: 0.95em;
  font-weight: 400;
  letter-spacing: 0.5px;
  color: rgba(240, 248, 255, 0.9);
  text-shadow: 0px 1px 2px rgba(0, 0, 0, 0.6);
}

.globe-visual-container {
  width: 75px;
  height: 75px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lottie-loading {
  font-size: 10px;
  color: #aaa;
}
</style>