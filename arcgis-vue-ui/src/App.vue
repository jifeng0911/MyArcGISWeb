<template>
  <div class="dashboard-layout">
    <div v-if="operationStatus" :class="['operation-status-banner', operationStatus.type]">
      <p>{{ operationStatus ? operationStatus.message : 'No message' }}</p>
      <button @click="clearOperationStatus" class="close-banner-btn" aria-label="关闭消息">×</button>
    </div>
    <div class="page-content-wrapper">
      <aside class="left-sidebar">
        <UserAvatar />
        <UserProfileWidget />
      </aside>

      <div class="main-panel">
        <div class="main-panel-top-row">
          <div class="center-greeting-verse">
            <HeaderGreeting />
            <DynamicVerse />
          </div>
          <div class="clock-area">
            <ClockWidget />
          </div>
        </div>
        <main class="main-content-area-cards">
          <h2 v-if="showMainContentTitle" class="section-title">ArcGIS 功能模块</h2>
          <div class="project-path-input-container">
            <label for="aprxPathInput" class="project-path-label">当前工程 (.aprx) 路径:</label>
            <input
              type="text"
              id="aprxPathInput"
              class="project-path-input"
              v-model="currentAprxPath"
              placeholder="例如：D:/GIS_Projects/MyProject.aprx 或 \\server\share\project.aprx"
            >
          </div>
          <div class="cards-grid">
            <ExampleCard1 title="新建工程" emojiIcon="✨" :action="() => handleToolAction('新建工程')" />
            <ExampleCard1 title="打开工程" emojiIcon="📁" :action="() => handleToolAction('打开工程')" />
            <ExampleCard1 title="缓冲区分析" emojiIcon="⭕" :action="() => handleToolAction('缓冲区分析')" />
            <ExampleCard1 title="叠加分析" emojiIcon="➕" :action="() => handleToolAction('叠加分析')" />
            <ExampleCard1 title="导出地图" emojiIcon="🗺️" :action="() => handleToolAction('导出地图')" />
            <ExampleCard1 title="数据转换" emojiIcon="🔄" :action="() => handleToolAction('数据转换')" />

          </div>
        </main>

      </div>
    </div>

    <footer class="dashboard-footer">
      <p>&copy; {{ currentYear }} 钟情于风的WebGIS项目</p>
    </footer>

    <BaseModal
      :show="isModalVisible"
      :title="modalTitle"
      @close="closeModal"
      @submit="handleModalSubmit"
      :maxWidth="modalMaxWidth"
      :isSubmitting="isSubmitting"
    >
      <template #body>
        <component :is="currentFormComponent" ref="dynamicForm" :availableLayers="mapLayersForModal" />
      </template>
    </BaseModal>
  </div>
</template>

<script>
// 导入所有需要的组件
import HeaderGreeting from './components/HeaderGreeting.vue';
import ClockWidget from './components/ClockWidget.vue';
import DynamicVerse from './components/DynamicVerse.vue';
import ExampleCard1 from './components/ExampleCard1.vue';
import UserAvatar from './components/UserAvatar.vue';
import UserProfileWidget from './components/UserProfileWidget.vue';
import BaseModal from './components/BaseModal.vue';
import BufferAnalysisForm from './components/BufferAnalysisForm.vue';
import ExportMapForm from './components/ExportMapForm.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    HeaderGreeting,
    ClockWidget,
    DynamicVerse,
    ExampleCard1,
    UserAvatar,
    UserProfileWidget,
    BaseModal,
    BufferAnalysisForm,
    ExportMapForm
  },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      showMainContentTitle: true,
      isModalVisible: false,
      modalTitle: '',
      currentAprxPath: '',
      currentFormComponent: null,
      modalMaxWidth: '550px',
      mapLayersForModal: [
        {id: 'points_of_interest', name: '兴趣点图层'},
        {id: 'roads_network', name: '道路网络'},
        {id: 'rivers_main', name: '主要河流'},
        {id: 'parcels', name: '地块数据'}
      ],
      isSubmitting: false,
      operationStatus: null, // 用于存储操作结果: { type: 'success'/'error', message: '...' }
    };
  },
  methods: {
    clearOperationStatus() { // 用于清除消息
      console.log('[App.vue] Clearing operation status.'); // 日志1
      this.operationStatus = null;
    },
    handleToolAction(toolName) {
      console.log(`[App.vue] handleToolAction called with: ${toolName}`); // 日志2
      if (this.isSubmitting) {
        console.log('[App.vue] Action prevented: isSubmitting is true.'); // 日志3
        return;
      }
      this.clearOperationStatus();
      if (!this.currentAprxPath.trim()) { // <<--- 确保在执行任何工具前都检查 aprxPath
        console.log('[App.vue] currentAprxPath is empty, setting error status.'); // 日志4
        this.operationStatus = { // <<--- 修改：使用消息横幅提示
          type: 'error', // 或者 'warning'/'info'
          message: '请先在上方输入有效的 ArcGIS Pro 工程 (.aprx) 文件路径！'
        };
        console.log('[App.vue] operationStatus set to:', JSON.parse(JSON.stringify(this.operationStatus))); // 日志5
        setTimeout(() => { if (this.operationStatus && this.operationStatus.message.includes('工程路径')) this.clearOperationStatus(); }, 5000);
        return;
      }
      if (toolName === '缓冲区分析') {
        this.modalTitle = '缓冲区分析参数';
        this.currentFormComponent = 'BufferAnalysisForm';
        this.modalMaxWidth = '550px';
        this.isModalVisible = true;
      } else if (toolName === '导出地图') {
        this.modalTitle = '导出地图参数';
        this.currentFormComponent = 'ExportMapForm'; // 加载新的表单组件
        this.modalMaxWidth = '600px'; // 可以为导出地图设置不同的宽度
        this.isModalVisible = true;
      } else {
        this.operationStatus = { // <<--- 修改：使用消息横幅提示
          type: 'info', // 表示一个提示信息
          message: `功能 "${toolName}" 正在开发中，敬请期待！`
        };
        setTimeout(() => { if (this.operationStatus && this.operationStatus.message.includes(toolName)) this.clearOperationStatus(); }, 5000);
      }
    },
    closeModal() {
      if (this.isSubmitting) return;
      this.isModalVisible = false;
      this.currentFormComponent = null;
    },
    async handleModalSubmit() {
      if (!this.$refs.dynamicForm || typeof this.$refs.dynamicForm.getFormData !== 'function') {
        console.error("无法获取动态表单的 getFormData 方法或表单组件未正确引用。");
        this.closeModal();
        this.isSubmitting = true;
        this.clearOperationStatus();
        return;
      }
      if (!this.currentAprxPath.trim()) {
        alert('错误：未指定 ArcGIS Pro 工程路径！');
        this.closeModal();
        return;
      }
      const formData = this.$refs.dynamicForm.getFormData();
      console.log('[App.vue] 步骤1: 从表单组件获取的 formData 类型:', typeof formData);
      console.log('[App.vue] 步骤1: 从表单组件获取的 formData 内容:', JSON.parse(JSON.stringify(formData)));
        if (formData && typeof formData === 'object' && !this.isSubmitting) { // <<--- 增加对 formData 类型的检查
          this.isSubmitting = true;
          const payload = Object.assign({}, {aprxPath: this.currentAprxPath}, formData);

          console.log('[App.vue] 步骤2: 最终构建的 payload (准备发送):', JSON.parse(JSON.stringify(payload)));

          let apiUrl = '';
          if (this.currentFormComponent === 'BufferAnalysisForm') {
            apiUrl = 'http://localhost:5000/api/gis/buffer_analysis';
          } else if (this.currentFormComponent === 'ExportMapForm') {
            apiUrl = 'http://localhost:5000/api/gis/export_map'; // <<--- 指向新的导出地图API
          } else {
            alert("未知的表单类型，无法提交！");
            this.isSubmitting = false;
            this.closeModal();
            return;
          }

          // --- ↓↓↓ 现在使用真实的 API 调用 ↓↓↓ ---
          try {
            console.log(`[App.vue] 步骤3: 发送 POST 请求到: ${apiUrl}，数据:`, JSON.parse(JSON.stringify(payload))); // <<--- 打印将要发送的数据
            const response = await axios.post(apiUrl, payload, {
              headers: {'Content-Type': 'application/json'}
            });

            console.log('[App.vue] 后端响应:', response.data);
            if (response.data && response.data.status === 'success') {
              alert(`操作成功！\n消息: ${response.data.message || '处理完成。'}\n输出路径: ${response.data.output_path || 'N/A'}`);
            } else {
              alert(`操作失败。\n错误: ${response.data ? response.data.message : '未知后端错误。'}`);
            }
          } catch (error) {
            console.error('[App.vue] 调用后端API时出错:', error);
            let errorMessage = '调用后端服务时发生网络或服务器错误。';
            if (error.response) {
              console.error("后端错误响应数据:", error.response.data);
              errorMessage += `\n错误码: ${error.response.status}. `;
              errorMessage += `\n后端消息: ${error.response.data.message || JSON.stringify(error.response.data)}`;
            } else if (error.request) {
              console.error("请求已发出但无响应:", error.request);
              errorMessage += "\n无法连接到后端服务，请检查网络或服务是否运行。";
            } else {
              errorMessage += `\n请求设置错误: ${error.message}`;
            }
            alert(errorMessage);
          } finally {
            this.isSubmitting = false;
            this.closeModal();
            console.log('[App.vue] handleModalSubmit finally block. Current operationStatus:', JSON.parse(JSON.stringify(this.operationStatus))); // 日志7
            if (this.operationStatus) { // 确保 operationStatus 不是 null 才设置定时器
              const currentMessage = this.operationStatus.message; // 保存当前消息
              setTimeout(() => {
                if (this.operationStatus && this.operationStatus.message === currentMessage) {
                  console.log('[App.vue] setTimeout in handleModalSubmit calling clearOperationStatus.'); // 日志8
                  this.clearOperationStatus();
                }
              }, 7000); // 7秒后自动清除
            }
          }
        // --- ↑↑↑ 真实的 API 调用结束 --- ↑↑↑
      } else if (this.isSubmitting) {
        console.log("[App.vue] 正在提交中，请稍候...");

      }
    }
  }
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column; /* <<--- 主轴设为垂直 */
  min-height: 100vh;     /* 确保布局至少和视口一样高 */
  max-width: 1800px;     /* 限制内容最大宽度 */
  margin: 0 auto;        /* 使内容在宽屏上居中 */
  box-sizing: border-box;
}
.operation-status-banner {
  padding: 12px 18px;
  border-radius: 6px; /* 更柔和的圆角 */
  margin: 0 0 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.18); /* 稍微增强阴影 */
  font-size: 0.9rem; /* 调整字体大小 */
  line-height: 1.4;
  position: relative;
  z-index: 100;
}
.operation-status-banner.success {
  background-color: #4CAF50; /* 一个标准绿色 */
  /* background-color: rgba(76, 175, 80, 0.9); */ /* 带透明度的绿色 */
  color: white;
  /* border: 1px solid #388E3C; */ /* 可选的边框 */
}
.operation-status-banner.error {
  background-color: #F44336; /* 一个标准红色 */
  /* background-color: rgba(244, 67, 54, 0.9); */
  color: white;
  /* border: 1px solid #D32F2F; */
}
.operation-status-banner.info {
  background-color: #2196F3; /* 一个标准蓝色 */
  /* background-color: rgba(33, 150, 243, 0.9); */
  color: white;
  /* border: 1px solid #1976D2; */
}
.operation-status-banner.warning {
  background-color: #FFC107; /* 一个标准黄色 */
  color: #212529; /* 深色文字在黄色上更清晰 */
  /* border: 1px solid #FFA000; */
}
.operation-status-banner p {
  margin: 0;
  flex-grow: 1;
  padding-right: 10px; /* 给文字和关闭按钮一些间距 */
}
.close-banner-btn {
  background: none;
  border: none;
  color: inherit; /* 继承父级的文字颜色 */
  font-size: 1.6em; /* 增大关闭按钮 */
  font-weight: bold;
  line-height: 1;
  cursor: pointer;
  opacity: 0.8;
  padding: 0 0 0 10px; /* 增加点击区域 */
}
.close-banner-btn:hover {
  opacity: 1;
}

.page-content-wrapper { /* 新增：包裹侧边栏和主面板，用于左右布局和垂直伸展 */
  display: flex;        /* 内部使用 flex 实现左右分栏 */
  flex-grow: 1;         /* 让它占据 dashboard-layout 中除去页脚之外的所有垂直空间 */
  padding: 25px 30px;   /* 将页面主要内容的左右内边距放在这里 */
  gap: 30px;            /* 左边栏和主面板之间的间距 */
  width: 100%;          /* 确保撑满 .dashboard-layout （如果 .dashboard-layout 有宽度限制）*/
  box-sizing: border-box;
  min-width: 0; /* 防止内部 flex item 溢出 */
}

.left-sidebar {
  flex: 0 0 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 100px; /* 头像和饼图卡片的垂直间距 */
  padding-top: 8px; /* 轻微下移，与右侧顶部内容协调 */
  box-sizing: border-box;
}

.main-panel {
  flex-grow: 1; /* 主面板占据 .page-content-wrapper 中剩余的水平空间 */
  display: flex;
  flex-direction: column; /* 主面板内部元素垂直排列 */
  min-width: 0;
  box-sizing: border-box;
}

.main-panel-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-top: 5px; /* 与 .left-sidebar 的 padding-top 协调 */
  flex-shrink: 0;
  /* width: 100%; */ /* 它会自然撑满 .main-panel */
  box-sizing: border-box;
}

.center-greeting-verse {
  flex-grow: 1;
  text-align: center;
  margin-left: 0;
  padding: 0 20px;
}

.clock-area {
  flex-shrink: 0;
  padding-top: 5px;
}

.main-content-area-cards {
  flex-grow: 1; /* 卡片区域占据主面板剩余的垂直空间 */
  width: 100%;
  box-sizing: border-box;
}

.section-title {
  font-size: 1.65em;
  font-weight: 500;
  color: #E8ECF3;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.55);
  margin-bottom: 22px;
  text-align: left;
  padding-left: 0;
}
.project-path-input-container {
  margin-bottom: 25px; /* 与下方 cards-grid 的间距 */
  padding: 15px 20px;  /* 内边距可以适当调整 */
  background-color: rgba(255, 255, 255, 0.6); /* 比之前更深一点的背景，与卡片区协调 */
  border-radius: 8px;
  box-sizing: border-box;
  /* width: 100%; */ /* 它会自然撑满其父容器 .main-content-area-cards (如果父容器没有左右padding) */
                  /* 或者你可以给它一个 max-width，例如 max-width: 700px; margin: 0 auto 25px auto; 使其居中 */
  max-width: 75%; /* 或者相对于父容器的百分比宽度 */
  margin-left: auto; /* 如果设置了 max-width，这两行使其居中 */
  margin-right: auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.project-path-label {
  display: block;
  font-size: 0.9em;
  color: #495057; /* 调整标签文字颜色 */
  margin-bottom: 8px;
  font-weight: 500;
  text-shadow: 0 1px 1px rgba(0,0,0,0.2);

}

.project-path-input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(10, 15, 35, 0.7); /* 更深的输入框背景 */
  color: #FFFFFF;
  font-size: 0.95em;
  box-sizing: border-box;
}
.project-path-input::placeholder {
  color: #858C99;
  opacity: 0.8;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 22px;
}

.dashboard-footer { /* 页脚现在是 .dashboard-layout 的直接子元素 */
  width: 100%;
  box-sizing: border-box;
  text-align: center;
  /* margin-top: auto; */ /* 当其父级 .dashboard-layout 是 flex-column, 且中间内容区域 flex-grow:1 时，这个不再是必须的 */
  padding: 20px 30px;    /* 页脚自身的上下和左右内边距 */
  padding-top: 35px;     /* 与上方内容的最小间距 */
  color: rgba(230, 230, 230, 0.75);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0; /* 防止页脚被压缩 */
}

.dashboard-footer p {
  margin: 0;
  font-size: 0.9em;
}

</style>