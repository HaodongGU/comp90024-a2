import React, { useState, useEffect } from 'react';
import { Scatter, Line, Bar} from 'react-chartjs-2';
import "./Mastodon.scss"
import axios from "axios";

const ip = process.env.REACT_APP_IP;

function BarChart() {
  // Define the data attributes for the two datasets
  const data = {
    labels: ['Attribute 1', 'Attribute 2', 'Attribute 3', 'Attribute 4'],
    datasets: [
      {
        label: 'Dataset 1',
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 1,
        data: [10, 15, 7, 12], // Replace with your actual data values for Dataset 1
      },
      {
        label: 'Dataset 2',
        backgroundColor: 'rgba(255,99,132,0.4)',
        borderColor: 'rgba(255,99,132,1)',
        borderWidth: 1,
        data: [8, 12, 10, 9], // Replace with your actual data values for Dataset 2
      },
    ],
  };

  const options={
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: 'white', // Adjust color of y-axis labels
        },
      },
      x: {
        ticks: {
          color: 'white', // Adjust color of x-axis labels
        },
      },
    },
  }

  return (
    <div>
      <h2>Bar Chart</h2>
      <Bar data={data} options={options}/>
    </div>
  );
}

const Mastodon = () => {
  const [time, setTime] = useState(new Date());
  const [dataNum, setDataNum] = useState(0);
  
  const currentDate = new Date();
  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
      setDataNum((dataNum) => dataNum + 1);
      
      
      const testConnections = async () => {
        try {  
          let url = "http://"+ip+":5000/topics_all_proportion";
  
          const res = await axios.get(url);
          console.log("res data: ", res.data);
  
          // const tempData = res.data.data[0].topics_uniquetwts.topics;
          // // console.log("Tuples in scatter graph0: ", tempData);
          // // console.log("Tuples in scatter graph1: ", tempData[0]);
          // // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][1]);
          // // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][0]);
  
          // setUniqueTwitts(res.data.data[0].topics_uniquetwts.uniquetwts);
          // // console.log("Unique twts0: ", uniqueTwitts);
          // // console.log("Unique twts1: ", res.data.data[0].topics_uniquetwts.uniquetwts);
  
          // for (const item in tempData) {
          //   // console.log(`${item}: ${tempData[item]}`);
          //   // labelList.push(item);
          //   // Perform other operations on the key-value pairs
          //   data.labels.push(item);
          //   data.datasets[0].data.push(tempData[item]);
          // }
          // setTopics(data);
          // console.log("Data in bar: ", data);
          // console.log("Topics in bar: ", topics);
          // // console.log("Tuples in scatter graph1: ", tuples);
  
        } catch (err) {
          // setTopics(data);
          // setUniqueTwitts(0);
          console.log(err);
        }
      };
      testConnections();
      



    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  return (
    <div className='bg_mas'>
      <h1>Mastodon Status</h1>

      <h2>Our Mastodon Harvester is crawling data right now. </h2>

      <h2>We have crawled {dataNum} pieces of data before {time.toLocaleTimeString()}, {currentDate.toDateString()}.</h2>
      <BarChart/>
    </div>
  );
}
export default Mastodon;