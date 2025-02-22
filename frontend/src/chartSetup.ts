import {
  Chart,
  Filler,
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  RadialLinearScale,
} from "chart.js";
import annotationPlugin from "chartjs-plugin-annotation";
import ChartDataLabels from "chartjs-plugin-datalabels";

Chart.register(
  Filler,
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  RadialLinearScale,
  annotationPlugin,
  ChartDataLabels
);

Chart.defaults.color = "#f7f1e1";
Chart.defaults.plugins.legend.labels.color = "#f7f1e1";
Chart.defaults.plugins.tooltip.titleColor = "#f7f1e1";
Chart.defaults.plugins.tooltip.bodyColor = "#f7f1e1";
Chart.defaults.scale.ticks.color = "#f7f1e1";

export default Chart;
