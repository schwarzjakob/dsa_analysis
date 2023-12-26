import React from "react";
import { Bar } from "react-chartjs-2";
import ChartDataLabels from 'chartjs-plugin-datalabels';

const BarChart = ({ data }) => {
  if (!data || !data.datasets || data.datasets.length === 0) {
    return null; // Or some placeholder
  }

  // Color the first 5 bars green and the last 5 bars red
  const barColors = data.datasets[0].data.map((_, index) => {
    if (index < 5) return "#4BC0C0"; // Teal
    if (index >= data.datasets[0].data.length - 5) return "#FF9F40"; // Orange
    return 'blue'; // Default color for the middle bars
  });

  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: data.datasets[0].label,
        data: data.datasets[0].data,
        backgroundColor: barColors,
      },
    ],
  };

  const chartOptions = {
    plugins: {
        datalabels: {
          anchor: 'end',
          align: 'top',
          formatter: (value) => {
            return value === 0 ? '' : value;
          }, // Display the value as it is
        },
    },
    scales: {
      y: {
        type: "linear",
        display: true,
        position: "left",
        title: {
          display: true,
          text: data.datasets[0].label,
        },
      },
      x: {
        title: {
          display: true,
          text: "Talent",
        },
      },
    },
  };

  console.log(data)

  return <Bar data={chartData} options={chartOptions} plugins={[ChartDataLabels]}/>;
};

export default BarChart;
