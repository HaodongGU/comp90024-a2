import React, { useState, useEffect } from 'react';
import { Scatter, Line, Bar, Pie  } from 'react-chartjs-2';
import Plot from 'react-plotly.js';

import "./Mastodon.scss"
import axios from "axios";
import {
  Chart as Chart,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend, 
  registerables
} from 'chart.js';

Chart.register(
  // LineElement,
  // CategoryScale,
  // LinearScale,
  // PointElement,
  // Tooltip,
  // Legend
  ...registerables
);

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
        // ticks: {
        //   maxRotation: 90,
        //   minRotation: 90,
        //   autoSkip: false,
        //   fontSize: 16, // Adjust the font size for the labels
        // },
        // grid: {
        //   color: 'white', // Set the y-axis grid color here
        // },
        // ticks: {
        //   color: 'white', // Adjust color of y-axis labels
        // },
      },
      x: {
        ticks: {
          font: {
            size: 13, // Adjust the font size for the x-axis labels
          },
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          font: {
            size: 16, // Adjust the font size for the dataset labels
          },
        },
      },

      tooltip: {
        titleFont: {
          size: 16, // Adjust the font size for the marker text
        },
        bodyFont: {
          size: 16, // Adjust the font size for the marker text
        },
      }
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
      <h2>Proportions of Different Topics in Mastodon and Twitter Data</h2>
      <div style={{backgroundColor: 'white', color: 'black'}}>
        <Bar data={data} options={options}/>
      </div>
    </div>
  );
}

const BoxPlotChart = () => {
  // Define the data for two sets
  const [data, setData] = useState([]);
  // const browserWidth = window.innerWidth;
  // console.log("browser width: !!!!!!!!!!!!!!!!!!!",browserWidth);

  // let tempData0 = [
  //   {
  //     y: dataset1,
  //     type: 'box',
  //     name: 'Dataset 1',
  //     boxpoints: 'all',
  //     jitter: 0.3,
  //     pointpos: -1.8,
  //     marker: { color: 'rgba(255, 99, 132, 0.5)' },
  //     showlegend: false,

  //   },
  //   {
  //     y: dataset2,
  //     type: 'box',
  //     name: 'Dataset 2',
  //     boxpoints: 'all',
  //     jitter: 0.3,
  //     pointpos: -1.8,
  //     marker: { color: 'rgba(54, 162, 235, 0.5)' },
  //     showlegend: false,

  //   },
  // ];

  let tempData = [];

  useEffect(() => {
    const testConnections = async () => {
      try {
        let urlMast = "http://"+ip+":5000/mas_topic_sentiment";
        const res_mast_senti = await axios.get(urlMast);
        console.log("mastodon data of topic sentimet", res_mast_senti.data);

        let urlTwit = "http://"+ip+":5000/twt_topic_sentiment";
        const res_twit_senti = await axios.get(urlTwit);
        console.log("twitter data of topic sentiment", res_twit_senti.data);

        for (let key in res_mast_senti.data) {
          if (res_twit_senti.data.hasOwnProperty(key)){
            tempData.push({ // mastodone
              y: res_mast_senti.data[key],
              type: 'box',
              name: "Mas: "+key,
              x: key,
              boxpoints: 'all',
              jitter: 0.3,
              pointpos: -1.8,
              marker: { color: 'rgba(255, 99, 132, 0.5)' },
              showlegend: false,
              boxpoints: false,
              // // showticklabels: false,
              // text: "fuck",
            });

            tempData.push({ // twitter
              y: res_twit_senti.data[key],
              type: 'box',
              name: "Twt: "+key,
              x: key,
              boxpoints: 'all',
              jitter: 0.3,
              pointpos: -1.8,
              marker: { color: 'rgba(54, 162, 235, 0.5)' },
              showlegend: false,
              boxpoints: false,
            })
          }
        }
        console.log("Temp data for box chart: ", tempData);
        setData(tempData);
      } catch (err) {
        console.log(err);
      }
    };
    testConnections();
  }, []);
  

  // Define the layout for the chart
  const layout = {
    title: 'Sentiment Value of Different Topics',
    yaxis: { title: 'Sentiment Value' },
    showlegend: true,
    height: 600,
    width: 1340,
    margin: {
      // l: 50,
      // r: 20,
      b: 200,
      // t: 80,
      pad: 0,
    },
    xaxis: {
      // title: '',
      // showticklabels: false, // Hide the tick labels on the x-axis
      // tickvals: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36],
      // ticktext: [0, 0, 0, 0,0],
      // showtickprefix:"first",
      // tickprefix:"haha",
      tickangle: -45,
    },
  };

  return (
    <div style={{width:'75vw'}}>
      <h2>Sentiment Value of Different Topics</h2>
      <Plot data={data} layout={layout} />
    </div>
  );
};


const PieChart = (props) => {
  const colors = [
    '#FF6384', '#63FF84', '#84FF63', '#6384FF', '#8463FF', '#FF8463',
    '#1F77B4', '#AEC7E8', '#FF7F0E', '#FFBB78', '#2CA02C', '#98DF8A',
    '#D62728', '#FF9896', '#9467BD', '#C5B0D5', '#8C564B', '#C49C94',
    '#E377C2'
];
  const initialData = {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [
      {
        data: [300, 50, 100],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      },
    ],
  };
  const [selectedOption, setSelectedOption] = useState("");
  const [rawData, setRawData] = useState(initialData);
  const [allData, setAllData] = useState({});

  // console.log("INITIAL rawdata: ", rawData);
  const handleChange = (event) => {
    setSelectedOption(event.target.value);
  };

  useEffect(() => {
    const testConnections = async () => {
      try {
        let url = "";
        switch (props.source){
          case "Twitter":
            url = "http://"+ip+":5000/twttopic_sentiment";
            break;
          case "Mastodon":
            url = "http://"+ip+":5000/mastopic_sentiment";
            break;
        }
        const res = await axios.get(url);
        console.log("Data Source: ", props.source, ", data: ", res.data);
        setAllData(res.data);
        // console.log("tempTopics: ",tempTopics);
        // console.log("tempMastTopic: ",tempMastTopic);
        // console.log("tempTwitter: ",tempTwitter);
      } catch (err) {
        console.log(err);
      }
    };
    testConnections();
  }, []);

  useEffect(() => {
    let topics=[];
    let proportions=[];
    const intervalData = allData[selectedOption];
    console.log("src: ", props.source," interval: ", selectedOption, " interval data: ", intervalData);
  
    for(let key in intervalData) {
      if(intervalData.hasOwnProperty(key)) {
        console.log(key + " -> " + intervalData[key]);
        topics.push(key);
        proportions.push(intervalData[key]);
      }
    }
  
    const data = {
      labels: topics,
      datasets: [
        {
          data: proportions,
          backgroundColor: colors,
          hoverBackgroundColor: colors,
        },
      ],
    };
    setRawData(data);
    console.log("Data Source: ", props.source, ", raw data: ", rawData);
  }, [selectedOption]);

  const options={
    plugins: {
      legend: {
        labels: {
          color: 'white', // Set the label color here
          font: {
            size: 14 // Set the desired label text size
          }
        },
      },
      tooltip: {
        titleFont: {
          size: 16, // Adjust the font size for the marker text
        },
        bodyFont: {
          size: 16, // Adjust the font size for the marker text
        },
      }
    },
  }

  return (
    <div style={{flex:1}}>
      <p>Please choose a sentiment interval of <i><b>{props.source}</b></i> data: </p>
      <div >
        <select value={selectedOption} onChange={handleChange} style={{fontSize:'16px'}}>
          <option value="">Select a sentiment interval</option>
          <option value="-1_-0.5">sentiment interval: [-1, -0.5)</option>
          <option value="-0.5_0">sentiment interval: [-0.5, 0)</option>
          <option value="0_0.5">sentiment interval: [0, 0.5)</option>
          <option value="0.5_1">sentiment interval: [0.5, 1)</option>

        </select>
        {/* <p>Selected: {selectedOption}</p> */}
      </div>
      <div style={{ width: '100%'}}>
        <Pie data={rawData} options={options}/>
      </div>
    </div>
  );
};


const Mastodon = () => {
  const [time, setTime] = useState(new Date());
  const [newestMastodon, setNewestMastodon] = useState({"content":"","sentiment_score":0,"timestamp":"", "topics":[],"url":""});
  const [dataNum, setDataNum] = useState(0);
  
  const currentDate = new Date();
  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());      
      
      const testConnections = async () => {
        try {  
          let url_latest_data = "http://"+ip+":5000/mas_latest_doc";
          const res_latest_data = await axios.get(url_latest_data);
          // console.log("res latest Mastodon data: ", res_latest_data.data);
          setNewestMastodon(res_latest_data.data);

          let url_data_num = "http://"+ip+":5000/mas_total";
          const res_data_num = await axios.get(url_data_num);
          // console.log("res latest Mastodon data: ", res_data_num.data);
          setDataNum(res_data_num.data);
        } catch (err) {
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
      <br/>
      <BoxPlotChart />
      <br/>
      <h2 style={{marginBottom:"0px"}}>Proportions of Topics within Different Sentiment Intervals</h2>
      <div style={{display: "flex", marginTop: "0px"}}>
        <PieChart source="Twitter"/>
        <PieChart source="Mastodon"/>
      </div>
      
    </div>
    // <h1>hhh</h1>
  );
}
export default Mastodon;