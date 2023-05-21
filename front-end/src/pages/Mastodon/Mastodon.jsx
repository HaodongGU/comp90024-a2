import React from 'react';
import { Scatter, Line } from 'react-chartjs-2';

const Mastodon = () => {
  // Sample scatter data
  const scatterData = {
    datasets: [
      {
        label: 'Scatter',
        data: [
          { x: 1, y: 1 },
          { x: 2, y: 3 },
          { x: 3, y: 2 },
          { x: 4, y: 4 },
          { x: 5, y: 5 },
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.4)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Line data
  const lineData = {
    datasets: [
      {
        label: 'Line',
        data: [
          { x: 1, y: 2 },
          { x: 2, y: 3 },
          { x: 3, y: 4 },
          { x: 4, y: 5 },
          { x: 5, y: 6 },
        ],
        backgroundColor: 'rgba(255, 99, 132, 0.4)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Chart options
  const options = {
    responsive: true,
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
      },
      y: {
        type: 'linear',
        position: 'left',
      },
    },
  };
  

  return (
    <div>
      <Scatter data={scatterData} options={options} />
      <Line data={lineData} options={options} />
    </div>
  );
};

export default Mastodon;