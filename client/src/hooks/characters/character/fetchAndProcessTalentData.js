import axios from "axios";

export const fetchAndProcessTalentData = async (characterName, talentName) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/character_analysis/analyze-talent`,
      {
        characterName: characterName,
        talentName: talentName,
      }
    );

    const {
      talent_statistics,
      talent_line_chart,
      talent_investment_recommendation,
    } = response.data;

    // Handle the case where timestamps or scores might be undefined
    const labels =
      talent_line_chart?.timestamps?.map((ts) =>
        new Date(ts * 1000).toLocaleDateString()
      ) || [];

    const scores = Array.isArray(talent_line_chart?.scores)
      ? talent_line_chart.scores
      : [];

    // Safely round and format the statistics
    const roundedTalentStatistics = {
      attempts: talent_statistics?.attempts || 0,
      success_rate: Number(talent_statistics?.success_rate || 0).toFixed(2),
      avg_score: Number(talent_statistics?.avg_score || 0).toFixed(2),
      std_dev: Number(talent_statistics?.std_dev || 0).toFixed(2),
    };

    return {
      talentLineChartData: {
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
      talentStatistics: roundedTalentStatistics,
      talentRecommendation: talent_investment_recommendation,
    };
  } catch (error) {
    console.error("Error fetching and processing talent data", error);
    return {
      talentLineChartData: null,
      talentStatistics: null,
      talentRecommendation: null,
    };
  }
};
