import React from "react";
import { Pie } from "react-chartjs-2";
//import ChartDataLabels from 'chartjs-plugin-datalabels';

const PieChart = ({ items }) => {
  const chartData = {
    labels: items.map((item) => item.item),
    datasets: [
      {
        data: items.map((item) =>
          Math.round(
            (item.count / items.reduce((a, b) => a + b.count, 0)) * 100
          )
        ),
        backgroundColor: [
          "#FF6384", // Red
          "#36A2EB", // Blue
          "#FFCE56", // Yellow
          "#4BC0C0", // Teal
          "#9966FF", // Purple
          "#FF9F40", // Orange
          "#C9CBCF", // Light Grey
          "#77C34F", // Green
        ],
        hoverBackgroundColor: [
          "#FF6384", // Red
          "#36A2EB", // Blue
          "#FFCE56", // Yellow
          "#4BC0C0", // Teal
          "#9966FF", // Purple
          "#FF9F40", // Orange
          "#C9CBCF", // Light Grey
          "#77C34F", // Green
        ],
      },
    ],
  };

  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
      padding: 40,
    },
    plugins: {
      legend: {
        position: "right",
        // Disable the default click behavior on the legend
        onClick: (e) => false,
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const percentage =
              chartData.datasets[0].data[tooltipItem.dataIndex];
            return `Relative usage: ${percentage}%`;
          },
        },
      },
    },
  };

  return <Pie data={chartData} options={pieChartOptions} />;
};

export default PieChart;
