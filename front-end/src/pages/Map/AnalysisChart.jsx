import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import axios from "axios";
import 'chartjs-plugin-trendline';

import { Scatter, Line } from 'react-chartjs-2';
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
      return "Logarithmic Population Density (persons/km^2 in logarithmic scale)";
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
  const [correlation, setCorrelation] = useState(0);

  console.log("DataAnalysis: attrname: ", props.attrName);
  const labelName = "Analysis of " + props.attrName;
  useEffect(() => {
    const testConnections = async () => {
      try {
        let url = "http://"+ip+":5000/senti_"+props.attrName.toLowerCase();
        if (props.attrName=="Public Transport") url = "http://"+ip+":5000/senti_transport";

        let tupleName = "avgsenti_"+props.attrName.toLowerCase();
        if (props.attrName=="Public Transport") tupleName = "avgsenti_transport";

        const res = await axios.get(url);
        console.log("res data: ", res.data);

        setCorrelation(res.data.meta.correlation);
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

  

  const data = {
    datasets: [
      {
        label: labelName,
        data: tuples,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        pointRadius: 3,
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
      legend: {
        labels: {
          font: {
            size: 16 // Set the desired label text size
          }
        },
      },
    },

  };


  // Calculate regression line data
  const regressionData = calculateRegressionLine(data.datasets[0].data);

  // Helper function to calculate regression line
  function calculateRegressionLine(data) {
    const xData = data.map(point => point.x);
    const yData = data.map(point => point.y);

    const sumX = xData.reduce((sum, value) => sum + value, 0);
    const sumY = yData.reduce((sum, value) => sum + value, 0);
    const sumXX = xData.reduce((sum, value) => sum + value * value, 0);
    const sumXY = data.reduce((sum, point) => sum + point.x * point.y, 0);

    const n = data.length;
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const minX = Math.min(...xData);
    const maxX = Math.max(...xData);
    const minY = Math.min(...yData);
    const maxY = Math.max(...yData);

    const regressionLine = [
      { x: minX, y: slope * minX + intercept },
      { x: maxX, y: slope * maxX + intercept },
    ];

    return regressionLine;
  }

  const regressionOptions = {
    showLine: true,
    spanGaps: false,
    maintainAspectRatio: false,
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

  const regressionChartData = {
    datasets: [
      {
        label: "Regression Line",
        data: regressionData,
        backgroundColor: 'rgba(255, 99, 132, 0.4)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        showLine: true,
      },
      
    ],
  };


  const customStyles = {
    overlay: {
      zIndex: 1000, // Set the z-index to a high number
      backgroundColor: 'rgba(0, 0, 0, 0.75)' // Optional: set a semi-transparent background
    },
  };


  const chartData = {
    datasets: [
      
      regressionChartData.datasets[0],
      data.datasets[0],
    ],
  };

  return (
    

    <div>
      <Modal
        isOpen={props.modalIsOpen}
        onRequestClose={props.closeModal}
        contentLabel={labelName}
        style={customStyles}
      >
        <div className="modal-content">
          <div className="modal-body">
            <div style={{ width: '1000px', height: '500px' }}>
              <Scatter data={chartData} options={options} />
            </div>
            <p>The correlation between <b>{props.attrName}</b> and sentiment is {correlation.toFixed(5)}</p>
            <button onClick={() => props.closeModal()}>Close</button>
          </div>
        </div>

        
      </Modal>
    </div>
  );
};

export default AnalysisChart;
