import React from "react";
import { Line } from "react-chartjs-2";

const LineChart = ({ data }) => {
  // Safeguard against undefined or incorrectly structured data
  if (!data || !data.datasets || !data.datasets[0] || !data.labels) {
    return <div>No data available for the chart</div>;
  }

  const chartDataArray = data.datasets[0].data || [];

  const chartData = {
    labels: data.labels.map((_, index) => `${index + 1}`),
    datasets: [
      {
        data: chartDataArray,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Attempt",
        },
        grid: {
          color: (context) => {
            if (context.tick.value === 0) {
              return "rgba(255,255,255,1)";
            }
          },
        },
      },
      y: {
        title: {
          display: true,
          text: "Score",
        },
        grid: {
          color: (context) => {
            if (context.tick.value === 0) {
              return "rgba(255,255,255,1)";
            }
          },
        },
      },
    },
  };

  return <Line data={chartData} options={chartOptions} />;
};

export default LineChart;
