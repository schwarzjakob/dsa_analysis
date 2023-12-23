import React, { useState, useEffect } from "react";
import axios from "axios";
import { Pie, Line } from "react-chartjs-2";
import {
  Chart,
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";
import "chartjs-plugin-annotation";
import annotationPlugin from "chartjs-plugin-annotation";
import Header from "./Header.js";
import "./App.css"; // Import the CSS file for styles

// Register the necessary components for Chart.js
Chart.register(
  ArcElement,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  annotationPlugin
);

function CharacterData() {
  const [selectedCharacter, setSelectedCharacter] = useState("");
  const [selectedTalent, setSelectedTalent] = useState("");
  const [characters, setCharacters] = useState([]);
  const [talentData, setTalentData] = useState([]);
  const [traitCount, setTraitCount] = useState([]);
  const [traitsValues, setTraitsValues] = useState([]);
  const [categoryCount, setCategoryCount] = useState([]);
  const [lineChartData, setLineChartData] = useState(null);

  useEffect(() => {
    // Fetch characters for selection
    const fetchCharacters = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/characters");
        const characterNames = response.data.characters.map(
          (char) => char.name
        ); // Extract names from the response
        setCharacters(characterNames); // Set the state to the names
      } catch (error) {
        console.error("Error fetching characters", error);
      }
    };

    fetchCharacters();
  }, []);

  useEffect(() => {
    // Fetch character data once a character is selected
    if (selectedCharacter) {
      const fetchData = async () => {
        try {
          const response = await axios.get(
            `http://127.0.0.1:5000/talents/${selectedCharacter}`
          );
          const {
            talents,
            traits_relative,
            traits_values,
            categories_relative,
          } = response.data;
          setTalentData(processTalents(talents));
          setTraitCount(processTraits(traits_relative));
          setTraitsValues(processTraitsValues(traits_values));
          setCategoryCount(processCategoryCount(categories_relative));
        } catch (error) {
          console.error("Error fetching character data", error);
        }
      };
      fetchData();
    }
  }, [selectedCharacter]);

  const processTalents = (talents) => {
    const talentArray = Object.entries(talents).map(([talent, value]) => {
      return { item: talent, count: value };
    });

    talentArray.sort((a, b) => b.count - a.count);
    return talentArray;
  };

  const processTraits = (traits_relative) => {
    return Object.entries(traits_relative).map(([trait, relativeUsage]) => {
      return { item: trait, count: relativeUsage };
    });
  };

  const processTraitsValues = (traits_values) => {
    return Object.entries(traits_values).map(([trait, relativeUsage]) => {
      return { item: trait, count: relativeUsage };
    });
  };

  const processCategoryCount = (categories_relative) => {
    return Object.entries(categories_relative).map(
      ([category, relativeUsage]) => {
        return { item: category, count: relativeUsage };
      }
    );
  };

  const handleCharacterChange = (e) => {
    setSelectedCharacter(e.target.value);
    console.log(e);
  };

  // Function to handle talent row click
  const handleTalentClick = async (talentName) => {
    try {
      setSelectedTalent(talentName);
      console.log(selectedCharacter, talentName);

      const response = await axios.post(
        `http://127.0.0.1:5000/analyze-talent`,
        {
          characterName: selectedCharacter,
          talentName: talentName,
        }
      );
      // Assuming response.data is the data needed for the line chart
      setLineChartData({
        labels: response.data.map((_, index) => `Attempt ${index + 1}`),
        datasets: [
          {
            label: talentName,
            data: response.data,
            fill: {
              target: "origin",
              below: "rgb(180, 63, 63)",
              above: "rgb(75, 192, 192)",
            },
            borderColor: "rgb(75, 192, 192)",
            borderWidth: 2.5,
          },
        ],
      });
    } catch (error) {
      console.error("Error fetching talent line chart data", error);
    }
  };

  // Define a plugin to render text inside the pie slices (not used as too complicated)
  const pieChartPlugin = {
    id: "textInsideSlices",
    afterDraw(chart) {
      const ctx = chart.ctx;
      ctx.font = "12px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#f7f1e1"; // Adjust text color as needed

      chart.data.datasets.forEach((dataset, datasetIndex) => {
        const meta = chart.getDatasetMeta(datasetIndex);
        meta.data.forEach((arc, index) => {
          const model = arc.getProps(
            ["startAngle", "endAngle", "innerRadius", "outerRadius"],
            true
          );
          const middleAngle = (model.startAngle + model.endAngle) / 2;
          const middleRadius = (model.innerRadius + model.outerRadius) / 0.9;
          const posX = arc.x + Math.cos(middleAngle) * middleRadius;
          const posY = arc.y + Math.sin(middleAngle) * middleRadius;

          ctx.fillText(Math.round(dataset.data[index]) + " %", posX, posY);
        });
      });
    },
  };

  // Register the plugin with Chart.js
  Chart.register(pieChartPlugin);

  // Options for the pie chart
  const traitsPieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
      padding: 40,
    },
    plugins: {
      legend: {
        position: "right",
        // Disable the default click behavior on the legend
        onClick: (e) => false,
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const label = traitsRelativePieChart.labels[tooltipItem.dataIndex];
            const percentage = Math.round(
              traitsRelativePieChart.datasets[0].data[tooltipItem.dataIndex]
            );
            return `${label}: ${percentage}%`;
          },
        },
      },
    },
  };

  // Data for the traits pie chart
  const traitsRelativePieChart = {
    labels: traitCount.map((trait) => trait.item),
    datasets: [
      {
        data: traitCount.map((trait) => Math.round(trait.count * 100)),
        backgroundColor: [
          "#FF6384", // Red
          "#36A2EB", // Blue
          "#FFCE56", // Yellow
          "#4BC0C0", // Teal
          "#9966FF", // Purple
          "#FF9F40", // Orange
          "#C9CBCF", // Light Grey
          "#77C34F", // Green
        ],
        hoverBackgroundColor: [
          "#FF6384", // Red
          "#36A2EB", // Blue
          "#FFCE56", // Yellow
          "#4BC0C0", // Teal
          "#9966FF", // Purple
          "#FF9F40", // Orange
          "#C9CBCF", // Light Grey
          "#77C34F", // Green
        ],
      },
    ],
  };

  // Data for the category pie chart
  const categoriesRelativePieChart = {
    labels: categoryCount.map((category) => category.item),
    datasets: [
      {
        data: categoryCount.map((category) => Math.round(category.count * 100)),
        backgroundColor: [
          "#FF6384", // Red
          "#36A2EB", // Blue
          "#FFCE56", // Yellow
          "#4BC0C0", // Teal
          "#9966FF", // Purple
          "#FF9F40", // Orange
          "#C9CBCF", // Light Grey
          "#77C34F", // Green
        ],
        hoverBackgroundColor: [
          "#FF6384", // Red
          "#36A2EB", // Blue
          "#FFCE56", // Yellow
          "#4BC0C0", // Teal
          "#9966FF", // Purple
          "#FF9F40", // Orange
          "#C9CBCF", // Light Grey
          "#77C34F", // Green
        ],
      },
    ],
  };

  // Options for the categories pie chart
  const categoriesPieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
      padding: 40,
    },
    plugins: {
      legend: {
        position: "right",
        onClick: (e) => false,
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const label =
              categoriesRelativePieChart.labels[tooltipItem.dataIndex];
            const percentage = Math.round(
              categoriesRelativePieChart.datasets[0].data[tooltipItem.dataIndex]
            );
            return `${label}: ${percentage}%`;
          },
        },
      },
    },
  };

  // Then, use this options object when rendering the categories pie chart:
  <Pie data={categoriesRelativePieChart} options={categoriesPieChartOptions} />;

  const lineChartOptions = {
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

  return (
    <>
      <div>
        <Header />
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
                <Pie
                  data={traitsRelativePieChart}
                  options={traitsPieChartOptions}
                />
              </div>
              <div className="chart-container">
                {" "}
                {/* Container for the category chart */}
                <h2>Category Usage Distribution</h2>
                <Pie
                  data={categoriesRelativePieChart}
                  options={categoriesPieChartOptions}
                />
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
                      <th>Talent</th>
                      <th>Häufigkeit</th>
                    </tr>
                  </thead>
                  <tbody className="body-container">
                    {talentData.map((item, index) => (
                      <tr
                        className="talent-list-row"
                        key={index}
                        onClick={() => handleTalentClick(item.item)}
                      >
                        <td>{item.item}</td>
                        <td>{item.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {lineChartData && (
                <div className="line-chart-container">
                  <h2>{`Usage of ${selectedTalent}`}</h2>
                  <Line data={lineChartData} options={lineChartOptions} />
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
