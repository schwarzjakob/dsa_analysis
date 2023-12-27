import React from "react";
import { Line } from "react-chartjs-2";

const LineChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => `Attempt ${index + 1}`),
    datasets: [
      {
        data: data.map((index) => index),
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
      y: {
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
