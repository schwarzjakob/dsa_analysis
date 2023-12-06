import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Pie, Line } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';
import 'chartjs-plugin-annotation';
import annotationPlugin from 'chartjs-plugin-annotation';
import './CharacterData.css'; // Import the CSS file for styles
import Header from './Header.js'


// Register the necessary components for Chart.js
Chart.register(ArcElement, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, annotationPlugin);

function CharacterData() {
    const [talentData, setTalentData] = useState([]);
    const [traitData, setTraitData] = useState([]);
    const { characterName } = useParams();

    // New state variable for line chart data
    const [selectedTalent, setSelectedTalent] = useState(null);
    const [lineChartData, setLineChartData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/talents/${characterName}`);
                const { talents, traits } = response.data;
                setTalentData(processTalents(talents));
                setTraitData(processTraits(traits));
            } catch (error) {
                console.error('Error fetching data', error);
            }
        };

        fetchData();
    }, [characterName]);

    const processTalents = (talents) => {
        return talents.map(talent => {
            return { item: talent[0], count: talent[1] };
        });
    };

    const processTraits = (traits) => {
        return Object.entries(traits).map(([trait, relativeUsage]) => {
            return { item: trait, count: relativeUsage };
        });
    };

    // Function to handle talent row click
    const handleTalentClick = async (talentName) => {
        try {
            setSelectedTalent(talentName);

            const response = await axios.post(`http://127.0.0.1:5000/analyze-talent`, { characterName, talentName });
            // Assuming response.data is the data needed for the line chart
            setLineChartData({
                labels: response.data.map((_, index) => `Attempt ${index + 1}`),
                datasets: [{
                    label: talentName,
                    data: response.data,
                    fill: {
                        target: 'origin',
                        below: 'rgb(180, 63, 63)',
                        above: 'rgb(75, 192, 192)',
                    },
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 2.5
                }]
            });
        } catch (error) {
            console.error('Error fetching talent line chart data', error);
        }
    };


    // Define a plugin to render text inside the pie slices (not used as too complicated)
    const pieChartPlugin = {
        id: 'textInsideSlices',
        afterDraw(chart) {
            const ctx = chart.ctx;
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#f7f1e1'; // Adjust text color as needed

            chart.data.datasets.forEach((dataset, datasetIndex) => {
                const meta = chart.getDatasetMeta(datasetIndex);
                meta.data.forEach((arc, index) => {
                    const model = arc.getProps(['startAngle', 'endAngle', 'innerRadius', 'outerRadius'], true);
                    const middleAngle = (model.startAngle + model.endAngle) / 2;
                    const middleRadius = (model.innerRadius + model.outerRadius) / 0.9;
                    const posX = arc.x + Math.cos(middleAngle) * middleRadius;
                    const posY = arc.y + Math.sin(middleAngle) * middleRadius;

                    ctx.fillText(Math.round(dataset.data[index]) + ' %', posX, posY);
                });
            });
        }
    };



    // Register the plugin with Chart.js
    Chart.register(pieChartPlugin);

    // Options for the pie chart
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: 40
        },
        plugins: {
            legend: {
                position: 'right',
                // Disable the default click behavior on the legend
                onClick: (e) => false
            },
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        let label = pieData.labels[tooltipItem.dataIndex] || '';
                        if (label) {
                            label += ': ';
                        }
                        label += Math.round(pieData.datasets[0].data[tooltipItem.dataIndex]) + '%';
                        return label;
                    }
                }
            }
        }
    };

    // Data for the pie chart
    const pieData = {
        labels: traitData.map(trait => trait.item),
        datasets: [{
            data: traitData.map(trait => Math.round(trait.count * 100)),
            backgroundColor: [
                '#FF6384', // Red
                '#36A2EB', // Blue
                '#FFCE56', // Yellow
                '#4BC0C0', // Teal
                '#9966FF', // Purple
                '#FF9F40', // Orange
                '#C9CBCF', // Light Grey
                '#77C34F'  // Green
            ],
            hoverBackgroundColor: [
                '#FF6384', // Red
                '#36A2EB', // Blue
                '#FFCE56', // Yellow
                '#4BC0C0', // Teal
                '#9966FF', // Purple
                '#FF9F40', // Orange
                '#C9CBCF', // Light Grey
                '#77C34F'  // Green
            ]
        }]
    };

    const lineChartOptions = {
        scales: {
            y: {
                grid: {
                    color: (context) => {
                        console.log(context.tick.value)
                        if (context.tick.value === 0) {
                            return 'rgba(255,255,255,1)'
                        }
                    }

                }
            }
        }
    };

    return (
        <><div>
            <Header />
        </div>
            <div>
                <h1>{characterName}</h1>
                <div className='content-container'> {/* Flex container */}
                    <div className='chart-container'> {/* Container for the chart */}
                        <h2>Trait Usage Distribution</h2>
                        <Pie data={pieData} options={options} />
                    </div>
                    <div className='table-container'> {/* Container for the table */}
                        <h2>Top Talent List</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Talent</th>
                                    <th>Häufigkeit</th>
                                </tr>
                            </thead>
                            <tbody className='body-container'>
                                {talentData.map((item, index) => (
                                    <tr key={index} onClick={() => handleTalentClick(item.item)}>
                                        <td>{item.item}</td>
                                        <td>{item.count}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                </div>
                {lineChartData && (
                    <div className='line-chart-container'>
                        <h2>{`Usage of ${selectedTalent}`}</h2>
                        <Line data={lineChartData} options={lineChartOptions} />
                    </div>
                )}
            </div></>
            );
}

            export default CharacterData;
