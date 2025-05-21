<template>
  <transition name="modal-fade">
    <div v-if="show" class="modal-backdrop" @mousedown.self="handleBackdropClick">
      <div class="modal-content feng-style-card" :style="{ maxWidth: maxWidth }" role="dialog" aria-modal="true" :aria-labelledby="titleId">
        <header class="modal-header">
          <slot name="header">
            <h3 :id="titleId" class="modal-title">{{ title }}</h3>
          </slot>
          <button type="button" class="btn-close" @click="closeModal" aria-label="关闭模态框" :disabled="isSubmitting">×</button>
        </header>

        <section class="modal-body">
          <slot name="body">
            <p>这是模态框的默认内容。</p>
          </slot>
        </section>

        <footer class="modal-footer">
          <slot name="footer">
            <button type="button" class="btn-feng btn-feng-secondary" @click="closeModal" :disabled="isSubmitting">
              {{ closeButtonText }}
            </button>
            <button v-if="showSubmitButton" type="button" class="btn-feng btn-feng-primary" @click="submitModal" :disabled="isSubmitting">
              {{ isSubmitting ? '提交中...' : submitButtonText }}
            </button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'BaseModal',
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      default: '提示',
    },
    submitButtonText: {
      type: String,
      default: '确定',
    },
    closeButtonText: {
        type: String,
        default: '关闭'
    },
    showSubmitButton: {
        type: Boolean,
        default: true
    },
    maxWidth: {
      type: String,
      default: '500px',
    },
    closeOnBackdropClick: {
      type: Boolean,
      default: true
    },
    isSubmitting: { // 新增 prop，用于禁用按钮
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'submit'],
  data() {
    return {
      titleId: `modal-title-${Math.random().toString(36).substring(7)}`
    };
  },
  methods: {
    closeModal() {
      if (this.isSubmitting) return; // 如果正在提交，不允许通过按钮或背景点击关闭
      this.$emit('close');
    },
    submitModal() { // 方法名改为 submitModal 以避免与 prop 冲突（虽然Vue会自动处理）
      if (this.isSubmitting) return; // 防止重复提交
      this.$emit('submit');
    },
    handleEscKey(event) {
      if (event.key === 'Escape' && this.show && !this.isSubmitting) { // 检查 isSubmitting
        this.closeModal();
      }
    },
    handleBackdropClick() {
      if (this.closeOnBackdropClick && !this.isSubmitting) { // 检查 isSubmitting
        this.closeModal();
      }
    }
  },
  watch: {
    show(value) {
      if (value) {
        document.addEventListener('keydown', this.handleEscKey);
        // document.body.style.overflow = 'hidden'; // 可选：锁定背景滚动
      } else {
        document.removeEventListener('keydown', this.handleEscKey);
        // document.body.style.overflow = ''; // 可选：恢复背景滚动
      }
    }
  },
  mounted() {
    if (this.show) {
      document.addEventListener('keydown', this.handleEscKey);
      // if (this.isSubmitting) document.body.style.overflow = 'hidden';
    }
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscKey);
    // if (this.show) { // 确保在组件销毁时恢复滚动，如果之前锁定了
    //   document.body.style.overflow = '';
    // }
  }
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.65);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  /* 应用全局 .feng-style-card (浅色透明背景，深色文字) */
  width: 90%;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  max-height: 85vh;
  overflow: hidden; /* 确保圆角生效 */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.modal-title {
  margin: 0;
  font-size: 1.2em;
  font-weight: 600;
  color: #1a2533; /* 深色标题 (与 .feng-style-card h3/h4 一致) */
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.7em;
  line-height: 1;
  color: #777;
  cursor: pointer;
  padding: 0;
  opacity: 0.7;
}
.btn-close:hover {
  color: #333;
  opacity: 1;
}
.btn-close:disabled {
    cursor: not-allowed;
    opacity: 0.4;
}


.modal-body {
  padding: 20px 25px;
  overflow-y: auto;
  color: #333d52; /* 确保 body 内的默认文字也是深色 */
  flex-grow: 1;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: rgba(248, 249, 250, 0.7);
  border-bottom-left-radius: inherit; /* 继承父级的圆角 */
  border-bottom-right-radius: inherit;
}

.btn-feng { /* 这些按钮会使用 global.css 中的 button 样式 */ }
.btn-feng-primary { /* 这些按钮会使用 global.css 中的 button 样式 */ }
.btn-feng-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}
.btn-feng-secondary:hover {
  background-color: #5a6268;
}
/* 禁用按钮的通用样式 */
.btn-feng:disabled {
    cursor: not-allowed;
    opacity: 0.65;
}


/* 过渡动画 */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.25s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: all 0.25s ease-out;
}
.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: translateY(-20px) scale(0.98);
  opacity: 0;
}
</style>