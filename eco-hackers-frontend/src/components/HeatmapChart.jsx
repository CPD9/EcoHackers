import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { api } from '../services/api';

const HeatmapChart = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.getHourlyHeatmap();
        setData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load heatmap data');
        setLoading(false);
        console.error(err);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading heatmap...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data available</div>;

  // Create annotations for heatmap cells
  const annotations = [];
  for (let i = 0; i < data.days.length; i++) {
    for (let j = 0; j < data.hours.length; j++) {
      const value = data.values[i][j];
      const count = data.counts[i][j];
      
      if (count > 0 && value !== null) {
        annotations.push({
          x: data.hours[j],
          y: data.days[i],
          text: `${value.toFixed(1)}<br>n=${count}`,
          font: { color: value > 340 ? 'white' : 'black', size: 8 },
          showarrow: false
        });
      }
    }
  }

  return (
    <div className="chart-container">
      <h2>Hourly Temperature Heatmap</h2>
      <Plot
        data={[
          {
            z: data.values,
            x: data.hours.map(h => `${h}:00`),
            y: data.days,
            type: 'heatmap',
            colorscale: 'Viridis',
            showscale: true
          }
        ]}
        layout={{
          title: 'Temperature by Day and Hour',
          annotations: annotations,
          width: 900,
          height: 500,
          margin: { l: 80, r: 50, t: 100, b: 80 }
        }}
      />
    </div>
  );
};

export default HeatmapChart;