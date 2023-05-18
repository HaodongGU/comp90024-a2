import React, { useState } from 'react';
import Modal from 'react-modal';
import { Scatter } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

Modal.setAppElement('#root'); 

const xlabelName = (attrName) => {
  switch (attrName){
    case "Income":
      return "Income (AUD)";
    case "Age":
      return "Age (years old)";
    default:
      return "default value in xlabel";
  }

}

const AnalysisChart = (props) => {
  console.log("DataAnalysis: attrname: ", props.attrName);
  const labelName = "Analysis of " + props.attrName;
  const demo = [
    { x: 1, y: 2 },
    { x: 2, y: 4 },
    { x: 3, y: 1 },
    { x: 4, y: 5 },
    { x: 5, y: 3 },
  ];

  // const coordinates=??? // TODO: GET .......................................

  const data = {
    datasets: [
      {
        label: labelName,
        data: demo,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        pointRadius: 5,
        pointHoverRadius: 7,
      },
    ],
  };

  const options = {
    scales: {
      x: {
        title: {
          display: true,
          text: xlabelName(props.attrName),
          font: {
            size: 16, 
          },
        },
      },
      y: {
        title: {
          display: true,
          text: 'Sentiment Value',
          font: {
            size: 16, 
          },
        },
      },
    },
    plugins: {
      tooltip: {
        titleFont: {
          size: 16, 
        },
        bodyFont: {
          size: 14, 
        },
      },
    },
  };

  const customStyles = {
    overlay: {
      zIndex: 1000, // Set the z-index to a high number
      backgroundColor: 'rgba(0, 0, 0, 0.75)' // Optional: set a semi-transparent background
    },
  };

  return (
    <div>
      <Modal
        isOpen={props.modalIsOpen}
        onRequestClose={props.closeModal}
        contentLabel={labelName}
        style={customStyles}
      >
        <Scatter data={data} options={options} />
        <button onClick={() => props.closeModal()}>Close</button>
      </Modal>
    </div>
  );
};

export default AnalysisChart;
