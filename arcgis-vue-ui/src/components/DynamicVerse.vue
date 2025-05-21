<template>
  <div class="dynamic-verse-container">
    <p class="verse-text">{{ displayedText }}<span class="cursor" :class="{ 'blink': isCursorBlinking }">|</span></p>
  </div>
</template>

<script>
// <script> 部分保持不变
// ... (之前已提供的 script 内容) ...
export default {
  name: 'DynamicVerse',
  props: {
    verses: {
      type: Array,
      default: () => [
        "如果期盼和等待都会有结果，那一定非常非常美。",
        "重要的不是所站的位置，而是所朝的方向。",
        "生活就像海洋，只有意志坚强的人，才能到达彼岸。"
      ]
    },
    typeSpeed: { type: Number, default: 120 }, // 可以适当加快一点打字速度
    deleteSpeed: { type: Number, default: 60 }, // 加快删除速度
    delayAfterTyping: { type: Number, default: 2800 },
    delayAfterDeleting: { type: Number, default: 400 }
  },
  // ... (其余 script 内容不变) ...
  data() {
    return {
      displayedText: '',
      currentVerseIndex: 0,
      isDeleting: false,
      charIndex: 0,
      isCursorBlinking: true,
      timeoutId: null
    };
  },
  computed: {
    currentVerse() {
      return this.verses[this.currentVerseIndex];
    }
  },
  mounted() {
    this.startEffect();
  },
  beforeUnmount() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  },
  methods: {
    startEffect() {
      if (this.isDeleting) {
        if (this.charIndex > 0) {
          this.displayedText = this.currentVerse.substring(0, this.charIndex - 1);
          this.charIndex--;
          this.timeoutId = setTimeout(this.startEffect, this.deleteSpeed);
        } else {
          this.isDeleting = false;
          this.currentVerseIndex = (this.currentVerseIndex + 1) % this.verses.length;
          this.charIndex = 0;
          this.timeoutId = setTimeout(this.startEffect, this.delayAfterDeleting);
        }
      } else {
        if (this.charIndex < this.currentVerse.length) {
          this.displayedText += this.currentVerse.charAt(this.charIndex);
          this.charIndex++;
          this.isCursorBlinking = false;
          this.timeoutId = setTimeout(this.startEffect, this.typeSpeed);
        } else {
          this.isDeleting = true;
          this.isCursorBlinking = true;
          this.timeoutId = setTimeout(this.startEffect, this.delayAfterTyping);
        }
      }
    }
  }
}
</script>

<style scoped>
.dynamic-verse-container {
  padding: 5px 0; /* 调整上下内边距 */
  text-align: center;
  margin-bottom: 30px; /* 与主要内容区域的间距 */
  min-height: 40px; /* 根据字体大小调整，防止内容跳动 */
}

.verse-text {
  font-family: 'Noto Sans SC', 'Inter', sans-serif; /* 优先使用适合中文的 Noto Sans SC */
  font-size: 1.25em; /* 调整字体大小，应小于主问候语，但清晰可见 */
  color: rgba(230, 235, 240, 0.88); /* 柔和的浅白色 */
  line-height: 1.7;
  font-weight: 500; /* Regular 或 Medium (500) */
  text-shadow: 0px 1px 3px rgba(0, 0, 0, 0.55),
                0px 0px 8px rgba(0, 0, 0, 0.2);/* 文字阴影 */
  max-width: 650px; /* 限制诗句的最大宽度，避免过长，根据 Leleo 风格调整 */
  margin: 0 auto; /* 使其在容器内居中 */
  display: inline-block; /* 确保背景区域只包裹文字 */
  padding: 5px 10px; /* 给文字一点呼吸空间 */
  /* background-color: rgba(0,0,0,0.1); */ /* 可选：给诗句一个非常淡的背景条，如果需要的话 */
  /* border-radius: 4px; */
}

.cursor {
  font-weight: normal; /* 光标不需要特别粗 */
  margin-left: 1px;
  color: rgba(235, 235, 255, 0.9);
  position: relative;
  top: -1px; /* 微调光标位置 */
}

.cursor.blink {
  animation: blink-animation 1s steps(1, start) infinite; /* steps 让闪烁更干脆 */
}

@keyframes blink-animation {
  to {
    visibility: hidden;
  }
}
</style>