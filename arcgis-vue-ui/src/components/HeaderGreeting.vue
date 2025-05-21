<template>
  <div class="header-greeting-widget">
    <h2>{{ greetingMessage }}</h2>
    <p class="subtitle">准备好开始您的地理空间智能操作了吗？</p>
  </div>
</template>

<script>
// <script> 部分保持不变
export default {
  name: 'HeaderGreeting',
  data() {
    return {
      userName: "用户",
      greeting: "您好"
    };
  },
  computed: {
    greetingMessage() {
      return `${this.greeting}，${this.userName}！`;
    }
  },
  created() {
    this.setGreetingByTime();
  },
  methods: {
    setGreetingByTime() {
      const currentHour = new Date().getHours();
      if (currentHour < 6) {
        this.greeting = "凌晨好";
      } else if (currentHour < 12) {
        this.greeting = "早上好";
      } else if (currentHour < 14) {
        this.greeting = "中午好";
      } else if (currentHour < 18) {
        this.greeting = "下午好";
      } else {
        this.greeting = "晚上好";
      }
    }
  }
}
</script>

<style scoped>
.header-greeting-widget {
  text-align: center;
  padding: 10px 0; /* 上下内边距，左右由 App.vue 的 .top-center 控制 */
  margin-bottom: 5px; /* 与下方 DynamicVerse 的间距调小一些 */
  /* 这个组件本身不需要像卡片那样的背景，因为它主要是文字展示 */
}

.header-greeting-widget h2 { /* 主问候语 */
  font-family: 'Inter', 'Noto Sans SC', sans-serif; /* 使用新字体 */
  font-size: 3.5em;  /* Leleo 主页的问候语通常非常大，请根据实际效果调整 */
  font-weight: 700; /* Bold 或更粗，如 800 */
  color: #ffffff;
  margin-bottom: 8px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.65); /* 更强的阴影使其突出 */
  line-height: 1.2;
}

.header-greeting-widget .subtitle { /* 副标题 */
  font-family: 'Inter', 'Noto Sans SC', sans-serif; /* 使用新字体 */
  font-size: 1.1em; /* 副标题相对小一些 */
  color: #C7F3EF; /* 柔和的浅色 */
  font-weight: 400; /* Regular */
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
  margin-bottom: 0;
  line-height: 1.5;
  left: -10px;
}
</style>