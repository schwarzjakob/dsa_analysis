import React from "react";
import { Radar } from "react-chartjs-2";

interface TraitSpiderChartProps {
  characterData: any;
}

const TraitSpiderChart: React.FC<TraitSpiderChartProps> = ({
  characterData,
}) => {
  const traitsOrder = [
    { label: "CH", value: characterData?.charisma || 0 },
    { label: "FF", value: characterData?.fingerfertigkeit || 0 },
    { label: "GE", value: characterData?.gewandtheit || 0 },
    { label: "IN", value: characterData?.intuition || 0 },
    { label: "KL", value: characterData?.klugheit || 0 },
    { label: "KO", value: characterData?.konstitution || 0 },
    { label: "KK", value: characterData?.koerperkraft || 0 },
    { label: "MU", value: characterData?.mut || 0 },
  ];

  const data = {
    labels: traitsOrder.map((trait) => trait.label),
    datasets: [
      {
        data: traitsOrder.map((trait) => trait.value),
        backgroundColor: "rgba(103, 125, 183, 0.62)",
        tension: 0,
        pointRadius: 0,
        datalabels: {
          display: true,
          color: "#f7f1e1",
          font: {
            size: 14,
          },
          formatter: (value) => (value > 0 ? value : ""),
          anchor: "end",
          align: "inside",
        },
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        grid: {
          color: "rgba(247, 241, 225, 0.2)",
          circular: false,
        },
        angleLines: {
          color: "rgba(247, 241, 225, 0.2)", // Fixed typo: 2225 -> 225
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: 20,
        ticks: {
          stepSize: 5,
          display: false,
        },
        pointLabels: {
          color: "#f7f1e1",
          font: {
            size: 16,
          },
          padding: 15,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: false,
      },
      datalabels: {
        // Ensure global datalabels config doesn’t conflict
        display: false, // Disable global default to avoid conflicts
      },
    },
  };

  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        minHeight: "400px",
      }}
    >
      <Radar data={data} options={options} />
    </div>
  );
};

export default TraitSpiderChart;
