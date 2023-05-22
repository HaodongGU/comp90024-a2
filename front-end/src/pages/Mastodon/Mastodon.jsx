import React, { useState, useEffect } from 'react';
import { Scatter, Line, Bar} from 'react-chartjs-2';
import "./Mastodon.scss"
import axios from "axios";

const ip = process.env.REACT_APP_IP;

function BarChart() {
  const [topics, setTopics] = useState(['Attribute 1', 'Attribute 2', 'Attribute 3', 'Attribute 4']);
  const [mastPercentage, setMastPercentage] = useState([10, 15, 7, 12]);
  const [twitterPercentage, setTwitterPercentage] = useState([8, 12, 10, 9]);

  // Define the data attributes for the two datasets
  const data = {
    labels: topics,
    datasets: [
      {
        label: 'Mastodon Topics and Their Percentages',
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 1,
        data: mastPercentage, // Replace with your actual data values for Dataset 1
      },
      {
        label: 'Twitter Topics and Their Percentages',
        backgroundColor: 'rgba(255,99,132,0.4)',
        borderColor: 'rgba(255,99,132,1)',
        borderWidth: 1,
        data: twitterPercentage, // Replace with your actual data values for Dataset 2
      },
    ],
  };

  const options={
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'white', // Set the y-axis grid color here
        },
        ticks: {
          color: 'white', // Adjust color of y-axis labels
        },
      },
      x: {
        grid: {
          color: 'white', // Set the y-axis grid color here
        },
        ticks: {
          color: 'white', // Adjust color of x-axis labels
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: 'white', // Set the label color here
        },
      },
    },
  }

  useEffect(() => {
    const testConnections = async () => {
      try {
        let urlMast = "http://"+ip+":5000/mas_topics_proportion";
        const res_mast_percentage = await axios.get(urlMast);
        // console.log("mastodon data of topic percentage", res_mast_percentage.data);
        let tempTopics = [];
        let tempMastTopic = [];
        let tempTwitter = [];
        for (const item of res_mast_percentage.data){
          tempTopics.push(item.topic);
          tempMastTopic.push(item.proportion);
        }

        let urlTwit = "http://"+ip+":5000/topics_all_proportion";
        const res_twit_percentage = await axios.get(urlTwit);
        // console.log("twitter data of topic percentage", res_twit_percentage.data);
        for (const item of res_twit_percentage.data){
          tempTwitter.push(item.proportion);
        }
        // console.log("tempTopics: ",tempTopics);
        // console.log("tempMastTopic: ",tempMastTopic);
        // console.log("tempTwitter: ",tempTwitter);
        setTopics(tempTopics);
        setMastPercentage(tempMastTopic);
        setTwitterPercentage(tempTwitter);
      } catch (err) {
        console.log(err);
      }
    };
    testConnections();
  }, []);

  return (
    <div>
      <h2>Bar Chart</h2>
      <Bar data={data} options={options}/>
    </div>
  );
}

const Mastodon = () => {
  const [time, setTime] = useState(new Date());
  const [newestMastodon, setNewestMastodon] = useState({});
  const [dataNum, setDataNum] = useState(0);
  
  const currentDate = new Date();
  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());      
      
      const testConnections = async () => {
        try {  
          let url_latest_data = "http://"+ip+":5000/mas_latest_doc";
          const res_latest_data = await axios.get(url_latest_data);
          console.log("res latest Mastodon data: ", res_latest_data.data);
          setNewestMastodon(res_latest_data.data);

          // let url_data_num = "http://"+ip+":5000/mas_latest_doc";
          // const res_latest_data = await axios.get(url_data_num);
          // console.log("res latest Mastodon data: ", res_latest_data.data);
          // setNewestMastodon(res_latest_data);
  
          // const tempData = res.data.data[0].topics_uniquetwts.topics;
          // console.log("Tuples in scatter graph0: ", tempData);
          // console.log("Tuples in scatter graph1: ", tempData[0]);
          // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][1]);
          // console.log("Tuples in scatter graph2: ", tempData[0][tupleName][0]);
  
          // setUniqueTwitts(res.data.data[0].topics_uniquetwts.uniquetwts);
          // console.log("Unique twts0: ", uniqueTwitts);
          // console.log("Unique twts1: ", res.data.data[0].topics_uniquetwts.uniquetwts);
  
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
          // console.log("Tuples in scatter graph1: ", tuples);
  
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

      <h3>Our Mastodon Harvester is crawling data right now. </h3>
      <h3>We have crawled {dataNum} pieces of data until {time.toLocaleTimeString()}, {currentDate.toDateString()}.</h3>
      <br/>
      <h2>The latest crawled data is shown below:</h2>
      <div className='newest_data'>
        <h3>Timestamp:</h3>
        <p>{newestMastodon.timestamp}</p>
        <h3>Content: </h3>
        <p>{newestMastodon.content}</p>
        <h3>Sentiment Scores:</h3>
        <p>{newestMastodon.sentiment_score}</p>
        <h3>Topics:</h3>
        <ul>
          {newestMastodon.topics.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <b>url: </b>
        <a href={newestMastodon.url} target="_blank" rel="noopener noreferrer" style={{color: "gold"}}>
          {newestMastodon.url}
        </a>
        

      </div>

      <BarChart/>
    </div>
    // <h1>hhh</h1>
  );
}
export default Mastodon;