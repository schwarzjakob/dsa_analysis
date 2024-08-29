import axios from "axios";

export const fetchAndProcessData = async (characterName) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/character_analysis/talents/${characterName}`
    );
    const { talents, traits_relative, traits_values, categories_relative } =
      response.data;

    const processedTalents = processTalents(talents);
    const processedTraits = processTraits(traits_relative);
    const processedTraitsValues = processTraitsValues(traits_values);
    const processedCategoryCount = processCategoryCount(categories_relative);

    const attacksResponse = await axios.get(
      `http://127.0.0.1:5000/character_analysis/attacks/${characterName}`
    );
    const { attacks } = attacksResponse.data;
    const processedAttacks = processAttacks(attacks);

    return {
      talents: processedTalents,
      traits_relative: processedTraits,
      traits_values: processedTraitsValues,
      categories_relative: processedCategoryCount,
      attacks: processedAttacks,
    };
  } catch (error) {
    console.error("Error fetching and processing data", error);
    return {};
  }
};

const processTraits = (traits_relative) => {
  return traits_relative.map(([trait, relativeUsage]) => {
    return { item: trait, count: relativeUsage };
  });
};

const processTraitsValues = (traits_values) => {
  return traits_values.map(([trait, value1, value2, value3]) => {
    const avgValue = ((value1 || 0) + (value2 || 0) + (value3 || 0)) / 3;
    return {
      item: trait,
      count: avgValue ? parseFloat(avgValue.toFixed(2)) : 0,
    };
  });
};

const processCategoryCount = (categories_relative) => {
  return categories_relative.map(([category, relativeUsage]) => {
    return { item: category, count: relativeUsage };
  });
};

const processTalents = (talents) => {
  const talentArray = talents.map(
    ([talent, count, successRate, failureRate, avgScore, stdDev]) => {
      // Safely rounding success rate
      successRate = Number(successRate);
      const roundedSuccessRate = !isNaN(successRate)
        ? successRate.toFixed(2)
        : 0;

      // Safely rounding failure rate
      failureRate = Number(failureRate);
      const roundedFailureRate = !isNaN(failureRate)
        ? failureRate.toFixed(2)
        : 0;

      // Safely rounding average score
      avgScore = Number(avgScore);
      const roundedAvgScore = !isNaN(avgScore) ? avgScore.toFixed(2) : 0;

      // Safely rounding standard deviation
      stdDev = Number(stdDev);
      const roundedStdDev = !isNaN(stdDev) ? stdDev.toFixed(2) : 0;

      return {
        talent,
        talent_count: count,
        success_rate: roundedSuccessRate,
        failure_rate: roundedFailureRate,
        avg_score: roundedAvgScore,
        std_dev: roundedStdDev,
      };
    }
  );
  return talentArray;
};

const processAttacks = (attacks) => {
  const attackArray = attacks.map(
    ([attack, count, successRate, failureRate, avgScore, stdDev]) => {
      // Safely rounding success rate
      successRate = Number(successRate);
      const roundedSuccessRate = !isNaN(successRate)
        ? successRate.toFixed(2)
        : 0;

      // Safely rounding failure rate
      failureRate = Number(failureRate);
      const roundedFailureRate = !isNaN(failureRate)
        ? failureRate.toFixed(2)
        : 0;

      // Safely rounding average score
      avgScore = Number(avgScore);
      const roundedAvgScore = !isNaN(avgScore) ? avgScore.toFixed(2) : 0;

      // Safely rounding standard deviation
      stdDev = Number(stdDev);
      const roundedStdDev = !isNaN(stdDev) ? stdDev.toFixed(2) : 0;

      return {
        attack,
        attack_count: count,
        success_rate: roundedSuccessRate,
        failure_rate: roundedFailureRate,
        avg_score: roundedAvgScore,
        std_dev: roundedStdDev,
      };
    }
  );
  return attackArray;
};
