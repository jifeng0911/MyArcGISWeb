<template>
  <div class="buffer-analysis-form">
    <div class="form-group">
      <label for="inputLayer">输入图层:</label>
      <select id="inputLayer" v-model="form.inputLayer" class="form-control">
        <option disabled value="">请选择图层</option>
        <option v-for="layer in availableLayers" :key="layer.id" :value="layer.id">
          {{ layer.name }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="outputLayerName">输出图层名称:</label>
      <input type="text" id="outputLayerName" v-model="form.outputLayerName" class="form-control" placeholder="例如：buffer_result">
    </div>

    <div class="form-group">
      <label for="bufferDistance">缓冲区距离:</label>
      <input type="number" id="bufferDistance" v-model.number="form.bufferDistance" class="form-control" placeholder="例如：100">
    </div>

    <div class="form-group">
      <label for="distanceUnits">距离单位:</label>
      <select id="distanceUnits" v-model="form.distanceUnits" class="form-control">
        <option value="Meters">米 (Meters)</option>
        <option value="Kilometers">千米 (Kilometers)</option>
        <option value="Feet">英尺 (Feet)</option>
        <option value="Miles">英里 (Miles)</option>
      </select>
    </div>

    <div class="form-group">
      <label for="dissolveType">融合类型 (可选):</label>
      <select id="dissolveType" v-model="form.dissolveType" class="form-control">
        <option value="NONE">无 (NONE)</option>
        <option value="ALL">全部融合 (ALL)</option>
        {/* 如果需要更复杂的功能 */}
      </select>
    </div>
    </div>
</template>

<script>
export default {
  name: 'BufferAnalysisForm',
  props: {
    // 如果需要从父组件传入初始值或可选图层列表
    initialData: {
      type: Object,
      default: () => ({})
    },
    availableLayers: {
      type: Array,
      // 示例： default: () => [{id: 'layer1', name: '道路图层'}, {id: 'layer2', name: '河流图层'}]
      default: () => [
        {id: 'points_of_interest', name: '兴趣点'},
        {id: 'roads_network', name: '道路网'},
        {id: 'rivers_main', name: '主要河流'}
      ] // 实际应用中，这个列表可能来自后端或主应用的状态管理
    }
  },
  data() {
    return {
      form: {
        inputLayer: this.initialData.inputLayer || '',
        outputLayerName: this.initialData.outputLayerName || 'buffered_features',
        bufferDistance: this.initialData.bufferDistance || 100,
        distanceUnits: this.initialData.distanceUnits || 'Meters',
        dissolveType: this.initialData.dissolveType || 'NONE',
      }
    };
  },
  methods: {
    // 提供一个方法让父组件可以获取表单数据
    getFormData() {
      // 可以在这里进行表单验证
      if (!this.form.inputLayer) {
        alert('请选择输入图层！');
        return null;
      }
      if (!this.form.outputLayerName.trim()) {
        alert('请输入输出图层名称！');
        return null;
      }
      if (typeof this.form.bufferDistance !== 'number' || this.form.bufferDistance <= 0) {
        alert('请输入有效的缓冲区距离！');
        return null;
      }
      return { ...this.form };
    }
  }
}
</script>

<style scoped>
.buffer-analysis-form {
  /* 表单内元素的间距等 */
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 0.9em;
  color: #495057; /* 深灰色标签文字 */
}

.form-control {
  /* 这些输入框和下拉选择会继承 global.css 中的 input, select 样式 */
  /* 你可以在这里覆盖或补充特定于表单的样式 */
  width: 100%; /* 确保它们撑满容器 */
  border: 1px solid #ced4da; /* 确保边框颜色适合浅色背景 */
  background-color: #fff; /* 确保背景是白色 */
  color: #495057; /* 确保输入文字是深色 */
}

/* 如果需要，可以为特定类型的输入框调整样式 */
input[type="number"] {
  /* appearance: textfield; */ /* 隐藏数字输入框的上下箭头 (某些浏览器) */
}
</style>