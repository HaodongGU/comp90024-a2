import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import axios from "axios";

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
const ip = process.env.REACT_APP_IP;

const xlabelName = (attrName) => {
  switch (attrName){
    case "Income":
      return "Income (AUD)";
    case "Age":
      return "Age (years old)";
    case "Population":
      return "Population Density (persons/km^2)";
    case "Public Transport":
      return "Composite Accessibility Index";
    case "Sport":
      return "Number of Sport Facilities";
    case "Crime":
      return "Number of Crimes";
    default:
      return "default value in xlabel";
  }

}

const AnalysisChart = (props) => {
  const [tuples, setTuples] = useState([]);

  console.log("DataAnalysis: attrname: ", props.attrName);
  const labelName = "Analysis of " + props.attrName;

  const demo = [
    { x: 1, y: 2 },
    { x: 2, y: 4 },
    { x: 3, y: 1 },
    { x: 4, y: 5 },
    { x: 5, y: 3 },
  ];
  useEffect(() => {
    const testConnections = async () => {
      try {
        let url = "http://"+ip+":5000/senti_"+props.attrName.toLowerCase();
        if (props.attrName=="Public Transport") url = "http://"+ip+":5000/senti_transport";

        let tupleName = "avgsenti_"+props.attrName.toLowerCase();
        if (props.attrName=="Public Transport") tupleName = "avgsenti_transport";

        const res = await axios.get(url);
        console.log("res data: ", res.data);

        const tempData = res.data.data;
        // console.log("Tuples in scatter graph0: ", tempData);
        // console.log("Tuples in scatter graph1: ", tempData[0]);
        // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][1]);
        // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][0]);

        let tempTuples = [];
        for (let i=0; i<tempData.length; i++){
          tempTuples.push({
            'x': tempData[i][tupleName][1],
            'y': tempData[i][tupleName][0]
          })
        }
        // console.log("Tuples in scatter graph0: ", tempTuples);
        setTuples(tempTuples);
        // console.log("Tuples in scatter graph1: ", tuples);

      } catch (err) {
        console.log(err);
      }
    };
    testConnections();
  }, [props.attrName]);

  

  // const coordinates=??? // TODO: GET .......................................

  const data = {
    datasets: [
      {
        label: labelName,
        data: tuples,
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
