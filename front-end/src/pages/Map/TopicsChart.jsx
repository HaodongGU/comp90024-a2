import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import axios from "axios";
import { Scatter, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend, 
  registerables
} from 'chart.js';

ChartJS.register(
  // LineElement,
  // CategoryScale,
  // LinearScale,
  // PointElement,
  // Tooltip,
  // Legend
  ...registerables
);

Modal.setAppElement('#root'); 
const ip = process.env.REACT_APP_IP;

const TopicsChart = (props) => {
  const [topics, setTopics] = useState({});
  const [uniqueTwitts, setUniqueTwitts] = useState(0);

  // console.log("TopicsAnalysis: suburbName: ", props.suburbName);
  const labelName = "Twitter Topics of " + props.suburbName;

  // const data = {
  //   labels: ['Category A', 'Category B', 'Category C', 'Category D'],
  //   datasets: [
  //     {
  //       label: 'Frequency',
  //       data: [10, 20, 30, 15],
  //       backgroundColor: 'rgba(75, 192, 192, 0.6)', // Bar color
  //     },
  //   ],
  // };

  let data = {
    labels: [],
    datasets: [
      {
        label: 'Topic Percentage',
        data: [],
        backgroundColor: 'rgba(75, 192, 192, 0.6)', // Bar color
      },
    ],
  };

  useEffect(() => {
    const testConnections = async () => {
      try {
        console.log("topicsAnalysis: attrname: ", props.attrName, ", suburb: ", props.suburbName);

        let url = "http://"+ip+":5000/topics_uniquetwts/"+props.suburbName;

        const res = await axios.get(url);
        // console.log("res data: ", res.data);

        const tempData = res.data.data[0].topics_uniquetwts.topics;
        // console.log("Tuples in scatter graph0: ", tempData);
        // console.log("Tuples in scatter graph1: ", tempData[0]);
        // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][1]);
        // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][0]);

        setUniqueTwitts(res.data.data[0].topics_uniquetwts.uniquetwts);
        // console.log("Unique twts0: ", uniqueTwitts);
        // console.log("Unique twts1: ", res.data.data[0].topics_uniquetwts.uniquetwts);

        for (const item in tempData) {
          // console.log(`${item}: ${tempData[item]}`);
          // labelList.push(item);
          // Perform other operations on the key-value pairs
          data.labels.push(item);
          data.datasets[0].data.push(tempData[item]);
        }
        setTopics(data);
        console.log("Data in bar: ", data);
        console.log("Topics in bar: ", topics);
        // console.log("Tuples in scatter graph1: ", tuples);

      } catch (err) {
        setTopics(data);
        setUniqueTwitts(0);
        console.log(err);
      }
    };
    testConnections();
  }, [props.suburbName]);


  const options = {
    scales: {
      x: {
        title: {
          display: true,
          text: "Topics Name",
          font: {
            size: 16, 
          },
        },
      },
      y: {
        title: {
          display: true,
          text: 'Topics Percentage',
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
      zIndex: 10000, // Set the z-index to a high number
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
        <h2>Twitter Topics in {props.suburbName}</h2>
        <p>Total Unique Twitters in {props.suburbName}: {uniqueTwitts}</p>
        <Bar data={topics} options={options} />
        <button onClick={() => props.closeModal()}>Close</button>
      </Modal>
    </div>
  );
};

export default TopicsChart;
