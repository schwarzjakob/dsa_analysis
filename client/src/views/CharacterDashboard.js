import React, { useState, useEffect } from "react";

// Import custom hooks
import { fetchCharacters } from "../hooks/characters/fetchCharacters.js";
import { fetchAndProcessData } from "../hooks/characters/character/fetchAndProcessCharacterData.js";
import { fetchAndProcessTalentData } from "../hooks/characters/character/fetchAndProcessTalentData.js";
import { fetchAndProcessAttackData } from "../hooks/characters/character/fetchAndProcessAttackData.js";

import {
  Chart,
  Filler,
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
} from "chart.js";
import "chartjs-plugin-annotation";
import annotationPlugin from "chartjs-plugin-annotation";
import Home from "../components/layout/Home.js";
import "../App.css"; // Import the CSS file for styles

// import Chart modules
import LineChart from "../components/charts/LineChart.js";
import BarChart from "../components/charts/BarChart.js";
import PieChart from "../components/charts/PieChart.js";

// Register the necessary components for Chart.js
Chart.register(
  Filler,
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  annotationPlugin
);

// Set global default font color
Chart.defaults.color = "#f7f1e1";
Chart.defaults.plugins.legend.labels.color = "#f7f1e1";
Chart.defaults.plugins.tooltip.titleColor = "#f7f1e1";
Chart.defaults.plugins.tooltip.bodyColor = "#f7f1e1";
Chart.defaults.scale.ticks.color = "#f7f1e1";

function CharacterData() {
  // Character States
  const [characters, setCharacters] = useState([]); // State for the list of characters
  const [selectedCharacter, setSelectedCharacter] = useState(""); // State for the selected character

  // Trait States
  const [traitCount, setTraitCount] = useState([]); // State for the list of traits
  const [traitsValues, setTraitsValues] = useState([]); // State for the list of trait values

  // Category States
  const [categoryCount, setCategoryCount] = useState([]); // State for the list of categories

  // Talents States
  const [talentsData, setTalentsData] = useState([]); // State for the list of talents
  // Additional states for each bar chart
  const [successRateChartData, setSuccessRateChartData] = useState(null);
  const [avgScoreChartData, setAvgScoreChartData] = useState(null);
  // Add state variables for sort column and direction
  const [talentsSortDirection, setTalentsSortDirection] = useState("desc");
  const [attacksSortDirection, setAttackSortDirection] = useState("desc");

  // Talent States
  const [selectedTalent, setSelectedTalent] = useState(""); // State for the selected talent
  const [talentLineChartData, setTalentLineChartData] = useState(null); // State for the talent line chart data
  const [talentStatistics, setTalentStatistics] = useState(null); // State for the talent statistics
  const [talentRecommendation, setTalentRecommendation] = useState(null); // State for the talent recommendation

  // Attacks States
  const [attacksData, setAttacksData] = useState([]); // State for the list of attacks
  const [selectedAttack, setSelectedAttack] = useState(""); // State for the selected attack
  const [attackLineChartData, setAttackLineChartData] = useState(null); // State for the attack line chart data
  const [attackStatistics, setAttackStatistics] = useState(null); // State for the attack statistics

  useEffect(() => {
    // Fetch characters for selection
    const getCharacters = async () => {
      const characterNames = await fetchCharacters();
      setCharacters(characterNames); // Set the state to the names
    };

    getCharacters();
  }, []);

  useEffect(() => {
    // Fetch character data once a character is selected
    const getData = async () => {
      const data = await fetchAndProcessData(selectedCharacter);
      setTalentsData(data.talents);
      setTraitCount(data.traits_relative);
      setTraitsValues(data.traits_values);
      setCategoryCount(data.categories_relative);
      setAttacksData(data.attacks);
    };

    if (selectedCharacter) {
      getData();
    }
  }, [selectedCharacter]);

  useEffect(() => {
    // Process data for bar charts
    if (talentsData.length > 0) {
      const filteredTalents = talentsData.filter(
        (talent) => talent.talent_count >= 10
      );

      const sortedBySuccessRate = [...filteredTalents].sort(
        (a, b) => b.success_rate - a.success_rate
      );

      const sortedByAvgScore = [...filteredTalents].sort(
        (a, b) => b.avg_score - a.avg_score
      );

      // Determine the count for top and bottom talents
      let topCount = Math.min(5, Math.ceil(filteredTalents.length / 2));
      let bottomCount = Math.min(5, Math.floor(filteredTalents.length / 2));

      // Adjust count if 3rd and 6th elements are the same
      if (
        filteredTalents.length === 6 &&
        sortedBySuccessRate[2].success_rate ===
          sortedBySuccessRate[5].success_rate
      ) {
        topCount = 3;
        bottomCount = 2;
      }

      const topSuccess = sortedBySuccessRate.slice(0, topCount);
      const bottomSuccess = sortedBySuccessRate.slice(-bottomCount);

      const topAvgScore = sortedByAvgScore.slice(0, topCount);
      const bottomAvgScore = sortedByAvgScore.slice(-bottomCount);

      // Function to fill gaps for less than 10 talents
      const fillGaps = (array, count) => {
        while (array.length < count) {
          array.push({ talent: "", success_rate: null, avg_score: null });
        }
        return array;
      };

      setSuccessRateChartData({
        labels: [...fillGaps(topSuccess, 5), ...fillGaps(bottomSuccess, 5)].map(
          (talent) => talent.talent
        ),
        datasets: [
          {
            label: "Success Rate",
            data: [...topSuccess, ...bottomSuccess].map(
              (talent) => talent.success_rate || 0
            ),
            backgroundColor: "rgba(75, 192, 192, 0.5)",
          },
        ],
      });

      setAvgScoreChartData({
        labels: [
          ...fillGaps(topAvgScore, 5),
          ...fillGaps(bottomAvgScore, 5),
        ].map((talent) => talent.talent),
        datasets: [
          {
            label: "Average Score",
            data: [...topAvgScore, ...bottomAvgScore].map(
              (talent) => talent.avg_score || 0
            ),
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
        ],
      });
    }
  }, [talentsData]);

  const handleSort = (
    data,
    setData,
    sortKey,
    currentDirection,
    setDirection
  ) => {
    // Sort the data by the given key and direction
    const sortedData = [...data].sort((a, b) => {
      let valueA = a[sortKey];
      const valueB = b[sortKey];
      console.log(data);

      if (typeof valueA === "string") {
        // Sort by string
        return currentDirection === "asc"
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA);
      } else {
        // Sort by number
        return currentDirection === "asc" ? valueA - valueB : valueB - valueA;
      }
    });
    setData(sortedData);
    setDirection(currentDirection === "asc" ? "desc" : "asc");
  };

  const handleCharacterChange = (e) => {
    // Set the selected character and reset the data
    setSelectedCharacter(e.target.value);
    setSelectedTalent("");
    setTalentLineChartData(null);
    setTalentsData([]);
    setTalentStatistics(null);
    setTalentRecommendation(null);
    setSelectedAttack("");
    setAttackLineChartData(null);
    setAttacksData([]);
    setAttackStatistics(null);
    console.log("Selected Character: ", e.target.value);
  };

  const handleTalentClick = async (talentName) => {
    // Set the selected talent and fetch the data
    setSelectedTalent(talentName);
    console.log(selectedCharacter, talentName);

    const data = await fetchAndProcessTalentData(selectedCharacter, talentName);
    setTalentLineChartData(data.talentLineChartData);
    setTalentStatistics(data.talentStatistics);
    setTalentRecommendation(data.talentRecommendation);
  };

  const handleAttackClick = async (attackName) => {
    // Set the selected attack and fetch the data
    setSelectedAttack(attackName);
    console.log(selectedCharacter, attackName);

    const data = await fetchAndProcessAttackData(selectedCharacter, attackName);
    setAttackLineChartData(data.attackLineChartData);
    setAttackStatistics(data.attackStatistics);
  };

  return (
    <>
      <div>
        <Home />
      </div>
      <div>
        <div className="character-select-container">
          <select onChange={handleCharacterChange} value={selectedCharacter}>
            <option value="">Select a Character</option>
            {characters.map((character, index) => (
              <option key={index} value={character}>
                {character}
              </option>
            ))}
          </select>
        </div>
        {selectedCharacter && (
          <div>
            {/* Trait Values Table*/}
            <div className="trait-values-container">
              <h2>Trait Values</h2>
              <table>
                <tbody>
                  <tr>
                    {/* Header Row: Trait Names */}
                    {traitsValues.map((trait, index) => (
                      <th key={index}>{trait.item}</th>
                    ))}
                  </tr>
                  <tr>
                    {/* Value Row: Trait Values */}
                    {traitsValues.map((trait, index) => (
                      <td key={index}>{trait.count}</td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="content-container">
              {" "}
              {/* Flex container */}
              <div className="chart-container">
                {" "}
                {/* Container for the trait chart */}
                <h2>Trait Usage Distribution</h2>
                <PieChart items={traitCount} />
              </div>
              <div className="chart-container">
                {" "}
                {/* Container for the category chart */}
                <h2>Category Usage Distribution</h2>
                <PieChart items={categoryCount} />
              </div>
            </div>
            <div className="content-container">
              <div className="chart-container">
                <h2>Best 5 and Worst 5 Talents By Successrate</h2>
                {successRateChartData && (
                  <BarChart data={successRateChartData} />
                )}
              </div>
              <div className="chart-container">
                <h2>Best 5 and Worst 5 Talents by Average score</h2>
                {avgScoreChartData && <BarChart data={avgScoreChartData} />}
              </div>
            </div>
            <div className="content-container">
              <div className="table-container">
                {" "}
                {/* Container for the table */}
                <h2>Top Talent List</h2>
                <table>
                  <thead>
                    <tr>
                      <th
                        onClick={() =>
                          handleSort(
                            talentsData,
                            setTalentsData,
                            "talent",
                            talentsSortDirection,
                            setTalentsSortDirection
                          )
                        }
                      >
                        Talent
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            talentsData,
                            setTalentsData,
                            "talent_count",
                            talentsSortDirection,
                            setTalentsSortDirection
                          )
                        }
                      >
                        Frequency
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            talentsData,
                            setTalentsData,
                            "success_rate",
                            talentsSortDirection,
                            setTalentsSortDirection
                          )
                        }
                      >
                        Success Rate
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            talentsData,
                            setTalentsData,
                            "failure_rate",
                            talentsSortDirection,
                            setTalentsSortDirection
                          )
                        }
                      >
                        Failure Rate
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            talentsData,
                            setTalentsData,
                            "avg_score",
                            talentsSortDirection,
                            setTalentsSortDirection
                          )
                        }
                      >
                        Average Score
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            talentsData,
                            setTalentsData,
                            "std_dev",
                            talentsSortDirection,
                            setTalentsSortDirection
                          )
                        }
                      >
                        Standard Deviation
                      </th>
                    </tr>
                  </thead>
                  <tbody className="body-container">
                    {talentsData.map((item, index) => (
                      <tr
                        className="talent-list-row"
                        key={index}
                        onClick={() => handleTalentClick(item.talent)}
                      >
                        <td>{item.talent}</td>
                        <td>{item.talent_count}</td>
                        <td>{item.success_rate}</td>
                        <td>{item.failure_rate}</td>
                        <td>{item.avg_score}</td>
                        <td>{item.std_dev}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {talentLineChartData && (
                <div className="table-container">
                  <div className="line-chart-container">
                    <h2>{`Usage of ${selectedTalent}`}</h2>
                    <LineChart data={talentLineChartData} />
                  </div>
                  {talentStatistics && (
                    <div className="talent-statistics-container">
                      <h2>{`Statistics for ${selectedTalent}`}</h2>
                      <table>
                        <tbody>
                          {Object.entries(talentStatistics).map(
                            ([statKey, statValue], index) => (
                              <tr key={index}>
                                <th>
                                  {statKey.charAt(0).toUpperCase() +
                                    statKey.slice(1)}
                                </th>
                                <td>{statValue}</td>
                              </tr>
                            )
                          )}
                          <tr>
                            <th>Recommendation</th>
                            <td>{talentRecommendation}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="content-container">
              <div className="table-container">
                {" "}
                {/* Container for the table */}
                <h2>Attack List</h2>
                <table>
                  <thead>
                    <tr>
                      <th
                        onClick={() =>
                          handleSort(
                            attacksData,
                            setAttacksData,
                            "attack",
                            attacksSortDirection,
                            setAttackSortDirection
                          )
                        }
                      >
                        Attack
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            attacksData,
                            setAttacksData,
                            "attack_count",
                            attacksSortDirection,
                            setAttackSortDirection
                          )
                        }
                      >
                        Frequency
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            attacksData,
                            setAttacksData,
                            "success_rate",
                            attacksSortDirection,
                            setAttackSortDirection
                          )
                        }
                      >
                        Success Rate
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            attacksData,
                            setAttacksData,
                            "failure_rate",
                            attacksSortDirection,
                            setAttackSortDirection
                          )
                        }
                      >
                        Failure Rate
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            attacksData,
                            setAttacksData,
                            "avg_score",
                            attacksSortDirection,
                            setAttackSortDirection
                          )
                        }
                      >
                        Average Score
                      </th>
                      <th
                        onClick={() =>
                          handleSort(
                            attacksData,
                            setAttacksData,
                            "std_dev",
                            attacksSortDirection,
                            setAttackSortDirection
                          )
                        }
                      >
                        Standard Deviation
                      </th>
                    </tr>
                  </thead>
                  <tbody className="body-container">
                    {attacksData.map((item, index) => (
                      <tr
                        className="talent-list-row"
                        key={index}
                        onClick={() => handleAttackClick(item.attack)}
                      >
                        <td>{item.attack}</td>
                        <td>{item.attack_count}</td>
                        <td>{item.success_rate}</td>
                        <td>{item.failure_rate}</td>
                        <td>{item.avg_score}</td>
                        <td>{item.std_dev}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {attackLineChartData && (
                <div className="table-container">
                  <div className="line-chart-container">
                    <h2>{`Usage of ${selectedAttack}`}</h2>
                    <LineChart data={attackLineChartData} />
                  </div>
                  {attackStatistics && (
                    <div className="talent-statistics-container">
                      <h2>{`Statistics for ${selectedAttack}`}</h2>
                      <table>
                        <tbody>
                          {Object.entries(attackStatistics).map(
                            ([statKey, statValue], index) => (
                              <tr key={index}>
                                <th>
                                  {statKey.charAt(0).toUpperCase() +
                                    statKey.slice(1)}
                                </th>
                                <td>{statValue}</td>
                              </tr>
                            )
                          )}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default CharacterData;