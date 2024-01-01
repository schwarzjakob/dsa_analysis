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

    // Adjust according to the total attempts
    const reordered_attack_statistics = {
      "Total Attempts": attack_statistics["Total Attempts"],
      Succeses: attack_statistics["Successes"],
      Failures: attack_statistics["Failures"],
      ...(attack_statistics["Total Attempts"] < 50
        ? { "Average Total": attack_statistics["Average Total"] }
        : {
            "Average First 30 Attempts":
              attack_statistics["Average First 30 Attempts"],
            "Average Last 30 Attempts":
              attack_statistics["Average Last 30 Attempts"],
          }),
      "Max Score": attack_statistics["Max Score"],
      "Min Score": attack_statistics["Min Score"],
      "Standard Deviation": attack_statistics["Standard Deviation"],
    };

    return {
      attackStatistics: reordered_attack_statistics,
      attackLineChartData: attack_line_chart,
    };
  } catch (error) {
    console.error("Error fetching attack line chart data", error);
    return {};
  }
};
