import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import "../App.css";
import Header from "../components/layout/Home.js";

const TraitsForSelectedTalents = () => {
  const [selectedTalents, setSelectedTalents] = useState([]);
  const [traitsData, setTraitsData] = useState({});
  const [talentsByCategory, setTalentsByCategory] = useState({});

  useEffect(() => {
    fetchTalentsOptions();
  }, []);

  useEffect(() => {
    const fetchTraitsData = async () => {
      try {
        const response = await fetch("/traits-for-selected-talents", {
          method: "POST",
          body: JSON.stringify({ talentsNameList: selectedTalents }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        setTraitsData(data);
      } catch (error) {
        console.error("Failed to fetch traits data", error);
      }
    };
    if (selectedTalents.length > 0) {
      fetchTraitsData();
    } else {
      setTraitsData({});
    }
  }, [selectedTalents]);

  const fetchTalentsOptions = async () => {
    try {
      const response = await fetch("/talents-options");
      const data = await response.json();
      const categories = data.talents.reduce((acc, talent) => {
        acc[talent.category] = acc[talent.category] || [];
        acc[talent.category].push(talent.talent);
        return acc;
      }, {});
      setTalentsByCategory(categories);
    } catch (error) {
      console.error("Failed to fetch talents options", error);
    }
  };

  const toggleTalentSelection = (talent) => {
    if (selectedTalents.includes(talent)) {
      setSelectedTalents(selectedTalents.filter((t) => t !== talent));
    } else {
      setSelectedTalents([...selectedTalents, talent]);
    }
  };

  const handleReset = () => {
    setSelectedTalents([]);
  };

  const selectAll = () => {
    const allTalents = Object.values(talentsByCategory).flat();
    setSelectedTalents(allTalents);
  };

  const chartData = {
    labels: Object.keys(traitsData),
    datasets: [
      {
        label: "Trait Count",
        data: Object.values(traitsData),
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  const renderCategoryTable = (category, talents) => (
    <div key={category} className="table-container">
      <h2>{category}</h2>
      <table>
        <tbody>
          {talents.map((talent) => (
            <tr
              key={talent}
              className={selectedTalents.includes(talent) ? "selected" : ""}
              onClick={() => toggleTalentSelection(talent)}
            >
              <td>{talent}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <>
      <div>
        <Header />
      </div>
      <div className="main-container">
        <div className="chart-container">
          <Bar data={chartData} />
        </div>
        <h2>Traits for Selected Talents</h2>
        <div className="content-container">
          {Object.entries(talentsByCategory).map(([category, talents]) =>
            renderCategoryTable(category, talents)
          )}
        </div>
        <button className="button" onClick={selectAll}>
          Select All
        </button>
        <button className="button" onClick={handleReset}>
          Reset
        </button>
      </div>
    </>
  );
};

export default TraitsForSelectedTalents;
