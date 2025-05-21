<template>
  <div class="export-map-form">
    <div class="form-group">
      <label for="emLayoutName">布局名称 (Layout Name):</label>
      <input type="text" id="emLayoutName" v-model.trim="form.layoutName" class="form-control" placeholder="例如：MainLayout 或 A3_Landscape">
      <small class="form-text">输入 ArcGIS Pro 工程中要导出的布局的确切名称。</small>
    </div>

    <div class="form-group">
      <label for="emOutputFormat">输出格式:</label>
      <select id="emOutputFormat" v-model="form.outputFormat" class="form-control">
        <option value="PDF">PDF</option>
        <option value="PNG">PNG</option>
        <option value="JPEG">JPEG</option>
        <option value="SVG">SVG</option>
        <option value="TIFF">TIFF</option>
      </select>
    </div>

    <div class="form-group">
      <label for="emOutputName">输出文件名称 (不含后缀):</label>
      <input type="text" id="emOutputName" v-model.trim="form.outputName" class="form-control" placeholder="例如：MyExportedMap">
      <small class="form-text">最终文件名将是此名称加上所选格式的后缀，例如 MyExportedMap.pdf。</small>
    </div>

    <div class="form-group">
      <label for="emDpi">分辨率 (DPI) (可选):</label>
      <input type="number" id="emDpi" v-model.number="form.dpi" class="form-control" placeholder="例如：300 (默认通常是96或根据布局设置)">
      <small class="form-text">通常用于栅格格式如 PNG, JPEG, TIFF。对于 PDF, SVG 可能影响较小或有不同处理方式。</small>
    </div>

    </div>
</template>

<script>
export default {
  name: 'ExportMapForm',
  props: {
    initialData: { // 如果需要从父组件预设值
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      form: {
        layoutName: this.initialData.layoutName || '',
        outputFormat: this.initialData.outputFormat || 'PDF',
        outputName: this.initialData.outputName || 'ExportedMap', // 默认输出文件名
        dpi: this.initialData.dpi || 300
      }
    };
  },
  methods: {
    getFormData() {
      if (!this.form.layoutName) {
        alert('请输入布局名称！');
        return null;
      }
      if (!this.form.outputName) {
        alert('请输入输出文件名称！');
        return null;
      }
      if (this.form.dpi !== null && (typeof this.form.dpi !== 'number' || this.form.dpi <= 0)) {
        alert('分辨率 (DPI) 必须是有效的大于0的数字。');
        return null;
      }
      // 只返回表单特定的数据，aprxPath 将由 App.vue 添加
      return { ...this.form };
    }
  }
}
</script>

<style scoped>
.export-map-form {
  /* 表单内元素的间距等 */
}

.form-group {
  margin-bottom: 20px; /* 增大表单组间距 */
}

.form-group label {
  display: block;
  margin-bottom: 8px; /* 标签和输入框的间距 */
  font-weight: 500;
  font-size: 0.9em;
  color: #333d52; /* 深色标签文字，因为模态框背景是浅色 */
}

.form-control {
  /* 这些输入框和下拉选择会继承 global.css 中的 input, select 样式 */
  /* 确保它们适合在浅色模态框背景上显示 */
  width: 100%;
  border: 1px solid #ced4da;
  background-color: #fff;
  color: #495057;
}

.form-text { /* 用于输入框下方的小提示文字 */
  display: block;
  font-size: 0.8em;
  color: #6c757d; /* 提示文字颜色 */
  margin-top: 5px;
}
</style>