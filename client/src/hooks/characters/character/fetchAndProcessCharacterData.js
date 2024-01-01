import axios from 'axios';

export const fetchAndProcessData = async (characterName) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/character_analysis/talents/${characterName}`
    );
    const {
      talents,
      traits_relative,
      traits_values,
      categories_relative,
    } = response.data;

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
      attacks: processedAttacks
    };
  } catch (error) {
    console.error("Error fetching and processing data", error);
    return {};
  }
};

// Function to process traits data
const processTraits = (traits_relative) => {
    return Object.entries(traits_relative).map(([trait, relativeUsage]) => {
      return { item: trait, count: relativeUsage };
    });
  };

  // Function to process traits values data
  const processTraitsValues = (traits_values) => {
    return Object.entries(traits_values).map(([trait, relativeUsage]) => {
      return { item: trait, count: relativeUsage };
    });
  };

  // Function to process category data
  const processCategoryCount = (categories_relative) => {
    return Object.entries(categories_relative).map(
      ([category, relativeUsage]) => {
        return { item: category, count: relativeUsage };
      }
    );
  };

// Function to process talents data
const processTalents = (talents) => {
    const talentArray = Object.entries(talents).map(([talent, metrics]) => {
      return { talent, ...metrics };
    });

    talentArray.sort((a, b) => a.order - b.order);

    return talentArray;
  };

// Function to process traits data
const processAttacks = (attacks) => {
    const attackArray = Object.entries(attacks).map(([attack, value]) => {
      return { attack: attack, attack_count: value };
    });

    attackArray.sort((a, b) => b.count - a.count);
    return attackArray;
  };