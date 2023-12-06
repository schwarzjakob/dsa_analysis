// TalentChart.js
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function TalentChart() {
    const [data, setData] = useState([]);

    useEffect(() => {
        // Fetch data from the backend and set it to state
        // Example: setData(fetchedData);
    }, []);

    return (
        <LineChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
    );
}

export default TalentChart;
