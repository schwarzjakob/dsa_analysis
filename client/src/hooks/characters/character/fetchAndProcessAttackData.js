import axios from "axios";

export const fetchAndProcessAttackData = async (characterName, attackName) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/character_analysis/analyze-attack`,
      {
        characterName: characterName,
        attackName: attackName,
      }
    );

    const { attack_statistics, attack_line_chart } = response.data;

    // Handle the case where timestamps or scores might be undefined
    const labels =
      attack_line_chart?.timestamps?.map((ts) =>
        new Date(ts * 1000).toLocaleDateString()
      ) || [];

    const scores = Array.isArray(attack_line_chart?.scores)
      ? attack_line_chart.scores
      : [];

    // Safely round and format the statistics
    const reordered_attack_statistics = {
      "Total Attempts": attack_statistics?.attempts || 0,
      Successes: Number(
        (attack_statistics?.success_rate || 0) *
          (attack_statistics?.attempts || 0)
      ).toFixed(2),
      Failures: Number(
        (1 - (attack_statistics?.success_rate || 0)) *
          (attack_statistics?.attempts || 0)
      ).toFixed(2),
      ...(attack_statistics?.attempts < 50
        ? {
            "Average Total": Number(attack_statistics?.avg_score || 0).toFixed(
              2
            ),
          }
        : {
            "Average First 30 Attempts": Number(
              attack_statistics?.avg_score || 0
            ).toFixed(2), // Placeholder logic
            "Average Last 30 Attempts": Number(
              attack_statistics?.avg_score || 0
            ).toFixed(2), // Placeholder logic
          }),
      "Max Score": Number(attack_statistics?.max_score || 0).toFixed(2), // Adjust if necessary
      "Min Score": Number(attack_statistics?.min_score || 0).toFixed(2), // Adjust if necessary
      "Standard Deviation": Number(attack_statistics?.std_dev || 0).toFixed(2),
    };

    return {
      attackStatistics: reordered_attack_statistics,
      attackLineChartData: {
        labels: labels,
        datasets: [
          {
            label: "Score",
            data: scores,
            fill: false,
            borderColor: "rgba(75, 192, 192, 1)",
          },
        ],
      },
    };
  } catch (error) {
    console.error("Error fetching and processing attack data", error);
    return {
      attackStatistics: null,
      attackLineChartData: null,
    };
  }
};
