import React from 'react';
import { Line } from 'react-chartjs-2';

const LineChart = ({ data }) => {
    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: data.datasets[0].label,
                data: data.datasets[0].data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            },
        ],
    };
    const chartOptions = {
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

    return <Line data={chartData} options={chartOptions}/>;
};

export default LineChart;
