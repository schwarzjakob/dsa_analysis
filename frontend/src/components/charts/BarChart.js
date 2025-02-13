import React from "react";
import { Bar } from "react-chartjs-2";
import ChartDataLabels from "chartjs-plugin-datalabels";

const BarChart = ({ data }) => {
  // Safeguard against undefined or incorrectly structured data
  if (!data || !data.datasets || !data.datasets[0] || !data.labels) {
    return <div>No data available for the chart</div>;
  }

  // Color the first 5 bars green and the last 5 bars red
  const barColors = data.datasets[0].data.map((_, index) => {
    if (index < 5) return "#4BC0C0"; // Teal
    if (index >= data.datasets[0].data.length - 5) return "#FF9F40"; // Orange
    return "blue"; // Default color for the middle bars
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
    layout: {
      padding: {
        top: 30,
      },
    },
    plugins: {
      datalabels: {
        anchor: "end",
        align: "top",
        formatter: (value) => {
          return value === 0 ? "" : value;
        }, // Display the value as it is
      },
      legend: {
        onClick: (e) => false,
        display: false,
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
        grid: {
          color: (context) => {
            if (context.tick.value === 0) {
              return "rgba(255,255,255,1)";
            }
          },
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

  return (
    <Bar data={chartData} options={chartOptions} plugins={[ChartDataLabels]} />
  );
};

export default BarChart;
