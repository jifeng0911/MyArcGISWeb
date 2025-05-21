<template>
  <div class="feng-tool-card white-transparent-card" @click="handleClick" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
    <div class="tool-card-icon-container">
      <span v-if="iconClass" :class="['tool-icon', iconClass]"></span>
      <span v-else-if="emojiIcon" class="tool-emoji-icon">{{ emojiIcon }}</span>
      <span v-else class="tool-icon placeholder-icon">🛠️</span>
    </div>
    <p class="tool-card-title">{{ title }}</p>
  </div>
</template>

<script>
export default {
  name: 'ExampleCard1',
  props: {
    title: {
      type: String,
      required: true
    },
    iconClass: { // 用于 Font Awesome 或其他 CSS 图标库的类名
      type: String,
      default: ''
    },
    emojiIcon: { // 用于简单的 Emoji 图标
      type: String,
      default: ''
    },
    action: { // 点击卡片时执行的动作
      type: Function,
      default: () => {
        // console.log('Tool card (ExampleCard1) clicked, no specific action defined for title:', this ? this.title : 'Unknown');
        // 由于 this 在箭头函数中不指向组件实例，如果需要访问 title，需要调整
        // default: function() { console.log('Tool card (ExampleCard1) clicked, no specific action defined for title:', this.title); }
      }
    }
  },
  data() {
    return {
      isHovered: false
    };
  },
  methods: {
    handleClick() {
      if (this.action) {
        this.action(); // 调用传入的 action
      } else {
        // 如果没有传入 action，可以有一个默认行为或提示
        console.log(`Card "${this.title}" clicked, but no action was provided.`);
      }
    }
  }
}
</script>

<style scoped>
.feng-tool-card.white-transparent-card {
  padding: 18px 15px;
  min-width: 130px;
  max-width: 170px;
  height: 110px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  overflow: hidden;
  border-radius: 14px;
  transition: transform 0.2s ease-out, box-shadow 0.2s ease-out;

  /* --- 白色透明背景 --- */
  background-color: rgba(255, 255, 255, 0.7); /* <<--- 纯白色，透明度调整为 0.80 (原0.78)，使其略微不透明 */
  /* backdrop-filter: blur(8px); */ /* 如果你的环境支持且需要，取消注释 */

  border: 1px solid rgba(0, 0, 0, 0.07);   /* 非常淡的深色边框 */
  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.09); /* 非常淡的深色阴影 */
}

.feng-tool-card.white-transparent-card:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 7px 22px rgba(0, 0, 0, 0.12);
}

.tool-card-icon-container {
  margin-bottom: 10px;
  line-height: 1;
}

.tool-icon, .tool-emoji-icon, .placeholder-icon {
  font-size: 2.5em; /* 保持或微调图标大小 */
  color: #2c3e50;   /* <<--- 图标颜色改为明确的深色 (深灰蓝) */
  text-shadow: none; /* 深色图标在浅色背景上通常不需要阴影 */
}

.tool-card-title {
  font-size: 0.9em;
  font-weight: 500; /* Medium weight */
  line-height: 1.3;
  margin: 0;
  color: #34495e;   /* <<--- 标题文字颜色改为明确的深色 (另一种深灰蓝) */
  text-shadow: none; /* 移除文字阴影 */

  /* 多行文本截断 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 2.34em; /* 0.9em * 1.3 * 2 (大约两行的高度) */
  /* 使用 word-break 来帮助长单词换行，虽然对于中文影响不大 */
  word-break: break-word;
}
</style>