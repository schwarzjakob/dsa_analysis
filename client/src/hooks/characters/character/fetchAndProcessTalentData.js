import axios from 'axios';

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

    // Adjust according to the total attempts
    const reorderd_talent_statistics = {
      "Total Attempts": talent_statistics["Total Attempts"],
      Succeses: talent_statistics["Successes"],
      Failures: talent_statistics["Failures"],
      ...(talent_statistics["Total Attempts"] < 50
        ? { "Average Total": talent_statistics["Average Total"] }
        : {
            "Average First 30 Attempts":
              talent_statistics["Average First 30 Attempts"],
            "Average Last 30 Attempts":
              talent_statistics["Average Last 30 Attempts"],
          }),
      "Max Score": talent_statistics["Max Score"],
      "Min Score": talent_statistics["Min Score"],
      "Standard Deviation": talent_statistics["Standard Deviation"],
    };

    return {
      talentLineChartData: talent_line_chart,
      talentStatistics: reorderd_talent_statistics,
      talentRecommendation: talent_investment_recommendation,
    };
  } catch (error) {
    console.error("Error fetching and processing talent data", error);
    return {};
  }
};