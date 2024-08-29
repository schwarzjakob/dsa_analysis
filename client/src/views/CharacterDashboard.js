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
      try {
        console.log("Fetching characters...");
        const characterNames = await fetchCharacters();
        console.log("Fetched characters: ", characterNames);
        setCharacters(characterNames); // Set the state to the names
      } catch (error) {
        console.error("Error fetching characters: ", error);
      }
    };

    getCharacters();
  }, []);

  useEffect(() => {
    if (selectedCharacter) {
      // Fetch character data once a character is selected
      const getData = async () => {
        try {
          console.log("Fetching data for character: ", selectedCharacter);
          const data = await fetchAndProcessData(selectedCharacter);
          console.log("Fetched data: ", data);
          setTalentsData(data.talents || []);
          setTraitCount(data.traits_relative || []);
          setCategoryCount(data.categories_relative || []);
          setAttacksData(data.attacks || []);
        } catch (error) {
          console.error("Error fetching data: ", error);
        }
      };

      getData();
    }
  }, [selectedCharacter]);

  // Separate useEffect for setting the traits when the character is selected
  useEffect(() => {
    if (selectedCharacter) {
      const selectedChar = characters.find(
        (char) => char.name === selectedCharacter
      );
      const charTraits = selectedChar ? selectedChar.traits : {};
      setTraitsValues(
        Object.entries(charTraits).map(([trait, value]) => ({ trait, value }))
      );
    }
  }, [selectedCharacter, characters]);

  useEffect(() => {
    if (talentsData.length > 0) {
      console.log("Processing talents data: ", talentsData);
      const filteredTalents = talentsData.filter(
        (talent) => talent.talent_count >= 10
      );

      const sortedBySuccessRate = [...filteredTalents].sort(
        (a, b) => b.success_rate - a.success_rate
      );

      const sortedByAvgScore = [...filteredTalents].sort(
        (a, b) => b.avg_score - a.avg_score
      );

      const topSuccess = sortedBySuccessRate.slice(0, 5);
      const bottomSuccess = sortedBySuccessRate.slice(-5);

      const topAvgScore = sortedByAvgScore.slice(0, 5);
      const bottomAvgScore = sortedByAvgScore.slice(-5);

      console.log(
        "Top and Bottom Success Talents: ",
        topSuccess,
        bottomSuccess
      );
      console.log(
        "Top and Bottom Average Score Talents: ",
        topAvgScore,
        bottomAvgScore
      );

      setSuccessRateChartData({
        labels: [...topSuccess, ...bottomSuccess].map(
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
        labels: [...topAvgScore, ...bottomAvgScore].map(
          (talent) => talent.talent
        ),
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
    } else {
      console.log("No talents data available to process.");
    }
  }, [talentsData]);

  const handleSort = (
    data,
    setData,
    sortKey,
    currentDirection,
    setDirection
  ) => {
    console.log(`Sorting data by ${sortKey} in ${currentDirection} order.`);
    // Sort the data by the given key and direction
    const sortedData = [...data].sort((a, b) => {
      let valueA = a[sortKey];
      const valueB = b[sortKey];

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
    console.log("Selected character: ", e.target.value);
    // Find the selected character and extract traits
    const selectedChar = characters.find(
      (char) => char.name === e.target.value
    );
    const charTraits = selectedChar ? selectedChar.traits : {};

    // Set the selected character and traits
    setSelectedCharacter(e.target.value);
    setTraitsValues(
      Object.entries(charTraits).map(([trait, value]) => ({ trait, value }))
    );
    setSelectedTalent("");
    setTalentLineChartData(null);
    setTalentsData([]);
    setTalentStatistics(null);
    setTalentRecommendation(null);
    setSelectedAttack("");
    setAttackLineChartData(null);
    setAttacksData([]);
    setAttackStatistics(null);
  };

  const handleTalentClick = async (talentName) => {
    console.log("Selected talent: ", talentName);
    // Set the selected talent and fetch the data
    setSelectedTalent(talentName);

    try {
      const data = await fetchAndProcessTalentData(
        selectedCharacter,
        talentName
      );
      console.log("Fetched talent data: ", data);
      setTalentLineChartData(data.talentLineChartData);
      setTalentStatistics(data.talentStatistics);
      setTalentRecommendation(data.talentRecommendation);
    } catch (error) {
      console.error("Error fetching talent data: ", error);
    }
  };

  const handleAttackClick = async (attackName) => {
    console.log("Selected attack: ", attackName);
    // Set the selected attack and fetch the data
    setSelectedAttack(attackName);

    try {
      const data = await fetchAndProcessAttackData(
        selectedCharacter,
        attackName
      );
      console.log("Fetched attack data: ", data);
      setAttackLineChartData(data.attackLineChartData);
      setAttackStatistics(data.attackStatistics);
    } catch (error) {
      console.error("Error fetching attack data: ", error);
    }
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
              <option key={index} value={character.name}>
                {character.name}
              </option>
            ))}
          </select>
        </div>
        {selectedCharacter && (
          <div>
            {/* Trait Values Table */}
            <div className="trait-values-container">
              <h2>Trait Values</h2>
              <table>
                <tbody>
                  <tr>
                    {traitsValues.map((trait, index) => (
                      <th key={index}>{trait.trait}</th>
                    ))}
                  </tr>
                  <tr>
                    {traitsValues.map((trait, index) => (
                      <td key={index}>{trait.value}</td>
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
