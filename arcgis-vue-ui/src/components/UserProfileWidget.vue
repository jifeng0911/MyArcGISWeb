<template>
  <div class="feng-profile-chart-card">
    <h4>主要技术栈</h4>
    <div class="pie-chart-wrapper-for-profile">
      <Pie v-if="chartDataLoaded" :data="chartData" :options="chartOptions" id="techStackPieChart" />
      <div v-else class="loading-placeholder">
        <p>(图表加载中...)</p>
      </div>
    </div>
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

export default {
  name: 'UserProfileWidget',
  components: {
    Pie
  },
  data() {
    // 确保这些百分比总和为 100 (或根据你的数据含义调整)
    const skillData = {
      'Vue.js': 35,
      'JavaScript (ES6+)': 25,
      'Python (ArcPy)': 20,
      'CSS3 & HTML5': 10,
      'GIS 平台': 5,
      '数据库': 5
    };

    const labels = Object.keys(skillData);
    const dataValues = Object.values(skillData);

    // 为你的技术栈定义颜色
    const colorMap = {
      'Vue.js': 'rgba(65, 184, 131, 0.85)',
      'JavaScript (ES6+)': 'rgba(247, 223, 30, 0.85)',
      'Python (ArcPy)': 'rgba(54, 162, 235, 0.85)',
      'CSS3 & HTML5': 'rgba(255, 107, 107, 0.85)',
      'GIS 平台': 'rgba(0, 122, 194, 0.85)',
      '数据库': 'rgba(153, 102, 255, 0.85)'
    };

    const backgroundColors = labels.map(label => colorMap[label] || 'rgba(200, 200, 200, 0.8)');
    const hoverBackgroundColors = labels.map(label => {
        const color = colorMap[label] || 'rgba(200,200,200,1)';
        return color.replace(/0\.\d+\)/, '0.95)');
    });

    return { // data() return 对象开始
      chartDataLoaded: false,
      chartInstance: null,
      chartData: { // chartData 属性开始
        labels: labels,
        datasets: [
          {
            label: '技术占比',
            data: dataValues,
            backgroundColor: backgroundColors,
            borderColor: 'rgba(100, 100, 100, 0.2)', // 边框改为深色，适应浅色背景
            borderWidth: 1.5,
            hoverBackgroundColor: hoverBackgroundColors,
            hoverBorderColor: 'rgba(80, 80, 80, 0.7)', // 悬停边框也改为深色
            hoverBorderWidth: 2,
            hoverOffset: 10
          }
        ]
      }, // chartData 属性结束, 后面有逗号

      chartOptions: { // chartOptions 属性开始
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false, // 图例不显示
          },
          title: {
            display: false,
          },
          tooltip: {
            enabled: true,
            backgroundColor: 'rgba(250, 250, 250, 0.92)', // 提示框背景改为浅色
            titleColor: '#2c3e50',                   // 提示框标题文字改为深色
            bodyColor: '#34495e',                    // 提示框内容文字改为深色
            borderColor: 'rgba(0, 0, 0, 0.15)',      // 提示框边框改为深色
            borderWidth: 1,
            padding: 10,
            cornerRadius: 8,
            usePointStyle: true,
            boxPadding: 4,
            bodyFont: { family: "'Inter', 'Noto Sans SC', sans-serif", size: 12 },
            titleFont: { family: "'Inter', 'Noto Sans SC', sans-serif", size: 13, weight: '600' },
            callbacks: {
              label: function(context) {
                let label = context.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed !== null) {
                  label += context.parsed + '%';
                }
                return label;
              }
            }
          }
        },
        cutout: '60%',
        elements: {
          arc: {
            borderWidth: 1.5,
          }
        },
        animation: {
          animateScale: true,
          animateRotate: true,
          duration: 1100,
          easing: 'easeInOutCubic'
        },
        onHover: (event, chartElement, chart) => {
            const canvas = chart.canvas;
            canvas.style.cursor = chartElement.length ? 'pointer' : 'default';
        },
        onClick: (event, elements, chart) => {
            if (elements.length > 0) {
                const firstPoint = elements[0];
                const label = chart.data.labels[firstPoint.index];
                const value = chart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index];
                console.log(`Clicked on Feng Chart: ${label} - ${value}%`);
            }
        }
      } // chartOptions 属性结束
    }; // data() return 对象结束
  }, // data() 方法结束, 后面有逗号
  mounted() {
    this.loadChartData();
  }, // mounted 方法结束, 后面有逗号
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
      this.chartInstance = null;
    }
  }, // beforeUnmount 方法结束, 后面有逗号
  methods: { // methods 对象开始
    loadChartData() {
      this.chartDataLoaded = true;
    }
  } // methods 对象结束
}; // export default 结束
</script>

<style scoped>
.feng-profile-chart-card {
  background-color: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(4px);
  border-radius: 16px;
  padding: 20px;
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.12);
}

.feng-profile-chart-card h4 {
  margin-bottom: 15px;
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  font-size: 1.15em;
  font-weight: 600;
  color: #E0E6F1;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.65); /* 浅色背景不需要文字阴影 */
}

.pie-chart-wrapper-for-profile {
  position: relative;
  width: 100%;
  max-width: 400px;
  height: 270px;    /* 保持我们之前调整的较大尺寸 */
  margin: 5px auto 0px auto;
}

.loading-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #b0b0c0;
  font-size: 0.9em;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

#techStackPieChart {
    display: block;
    box-sizing: border-box;
    height: 100% !important;
    width: 100% !important;
}
</style>