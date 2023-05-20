import React, { useState, useEffect } from "react";
import axios from "axios";
import { MapContainer, TileLayer, GeoJSON, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import suburbsData from './suburbsData.json'; 
import suburbsCentre from './suburb_centre.json'
import { Icon } from 'leaflet';
import { Marker as LeafletMarker } from 'react-leaflet';
import SadEmoji from "../../static/figure/sadEmoji.png";
import MarkerIncome from "../../static/figure/MarkerIncome.png"
import "./Map.scss"


const ip = process.env.REACT_APP_IP;
console.log("SuburbsMap env ip: ", process.env.REACT_APP_IP);

// define colors here. 
// const color5 = '#37FD12';
const color5 = '#4169E1';
// const color4 = '#C7EA46';
const color4 = '#5DAEFF';
// const color3 = '#9DC183';
const color3 = '#30D5C8';
const color2 = '#FA8072';
const color1 = '#FF0000';


// function used in suburb centre finding
function convertStrFormat(str) {
  var convertedString = str.toUpperCase();
  convertedString = convertedString.replace(/[^A-Za-z\s]/g, '')
  return convertedString;
}

const CustomMarker = (props) => {
  let IconName;
  switch (props.attrName){
    case "Income":
      IconName = MarkerIncome;
      break;
    default:
      IconName = SadEmoji;
      break;
  }
  
  const markerIcon = new Icon({
    iconUrl: IconName,
    iconSize: [32, 32],
  });

  // get all attributes
  const coodinates = props.suburbData.coordinates;
  const suburbName = props.suburbData.name;
  const value = props.suburbData.value;
  const valueName = props.suburbData.valueName;

  return (
    <LeafletMarker position={coodinates} icon={markerIcon}>
      <Popup>
        Suburb: {suburbName} <br /> 
        {valueName}: {value}
      </Popup>
    </LeafletMarker>
  )
};

const CustomMarkers = (props) => {
  const [outputTop, setOutputTop] = useState([]);
  const [outputBot, setOutputBot] = useState([]);

  const outputTopTemp = [];
  const outputBotTemp = [];

  var rawTop = [];
  var rawBot = {};
  var meta = {};
  var valueName = '';
  var output = [];

  // this hook get the suburb name, coordinates, value, value desc. Put them in a list
  useEffect(() => {
    const testConnections = async () => {
      try {
        const url = "http://"+ip+":5000/"+props.attrName.toLowerCase()+"_top_bot";
        const res = await axios.get(url);
        console.log("res data: ", res.data);
        rawTop = res.data['top data'];
        rawBot = res.data['bottom data'];
        meta = res.data['meta'];
        valueName = meta.value;
        console.log("rawTop data: ", rawTop);
        console.log("rawBot data: ", rawBot);
        console.log('value name: ', valueName);


        rawTop.forEach((item, index) => {
          if (suburbsCentre.hasOwnProperty(convertStrFormat(item.name))){
            console.log(convertStrFormat(item.name)+" is found in json file");
            outputTopTemp.push({
              'name': convertStrFormat(item.name),
              'value': item.value,
              'valueName': valueName,
              'coordinates': suburbsCentre[convertStrFormat(item.name)].center_coordinates
            });
          }
          else {
            console.log(convertStrFormat(item.name)+" is NOT found in json file");
          }

          console.log(`Item ${index + 1}: Name: ${item.name}, Value: ${item.value}`);
        });

        setOutputTop(outputTopTemp);
        console.log("output top temp: ", outputTopTemp);
        console.log("output top: ", outputTop);
        console.log("CustomMarkers data len: ", outputTop.length);
        // output = outputTop.map((data) => (
        //   <CustomMarker suburbData={data} attrName={props.attrName}/>
        // ));
        // console.log("output markers: ", output);
        // return output;
      } catch (err) {
        console.log(err);
      }
    };
    testConnections();
  }, [props.attrName]);



  // const demoPositions = [
  //   [-37.841076468482306, 144.97409770106265], 
  //   [-37.81935288212765, 144.9397721328937], 
  //   [-37.8158073266, 144.9810374616]];
  // const positions = demoPositions; //TODO: get request!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  
  console.log("CustomMarkers data len000000000000000: ", outputTop.length);
  output = outputTop.map((data) => (
    <CustomMarker suburbData={data} attrName={props.attrName}/>
  ));
  console.log("output markers: ", output);
  return output;
}

function SetPane() {
  const map = useMap();

  // Create pane with a high zIndex
  map.createPane('topPane');
  map.getPane('topPane').style.zIndex = '650';

  return null;
}

const SuburbsMap = (props) => {
  const [selectedSuburb, setSelectedSuburb] = useState(null);

  const handleSuburbClick = (event) => {
    // const suburbName = event.target.feature.properties.name;
    const suburbName = event.target.feature.properties.vic_loca_2;
    console.log("suburb clicked: ", suburbName);
    setSelectedSuburb(suburbName);
  };

  // choose color according to happiness level, and if it is chosen. 
  const colorChooser = (suburbName, selectedSuburb) => {
    if (suburbName===selectedSuburb){
      return '#F9A603'; // return blue as chosen
    }

    if (suburbsCentre[suburbName].hasOwnProperty("avgsenti")){
      const avgsenti = suburbsCentre[suburbName].avgsenti;
      if (avgsenti>0.6) { // happiest
        return color5
      }
      else if (avgsenti<=0.6 && avgsenti>0.2) {
        return color4
      }
      else if (avgsenti<=0.2 && avgsenti>-0.2) {
        return color3
      }
      else if (avgsenti<=-0.2 && avgsenti>-0.6) {
        return color2
      }
      else if (avgsenti<=-0.6) {
        return color1
      }
    }
    // console.error("Cannot find suburb ",suburbName, ", render with default color.");
    return '#ffffff'; // white? trans 
  }

  const geoJsonOptions = {
    style: (feature) => ({
      color: feature.properties.vic_loca_2 === selectedSuburb ? '#ff0000' : '#000000',
      weight: selectedSuburb === feature.properties.vic_loca_2 ? 3 : 1,
      // fillColor: feature.properties.vic_loca_2 === selectedSuburb ? '#ff0000' : '#3388ff',
      fillColor: colorChooser(feature.properties.vic_loca_2, selectedSuburb),
      fillOpacity: 0.5,
      // fillOpacity: 1,
    }),
    onEachFeature: (feature, layer) => {
      layer.on({
        click: handleSuburbClick,
      });
    },
  };

  return (
    <div style={{ height: "100%", width: "100%" }}>
      <div className="color_bar">
        <div className="color_bar_left">
          <b>Color: &nbsp;&nbsp;&nbsp;&nbsp;</b>
        </div>
        <div className="color_bar_right">
          <div style={{ height: "100%", width: "20%", backgroundColor: color1}}></div>
          <div style={{ height: "100%", width: "20%", backgroundColor: color2}}></div>
          <div style={{ height: "100%", width: "20%", backgroundColor: color3}}></div>
          <div style={{ height: "100%", width: "20%", backgroundColor: color4}}></div>
          <div style={{ height: "100%", width: "20%", backgroundColor: color5}}></div>
          <div style={{ height: "100%", width: "20%"}}></div>

        </div>
      </div>

      <div className="color_bar">
        <div className="color_bar_left">
          <b>Average Sentiment: &nbsp;&nbsp;&nbsp;&nbsp;</b>
        </div>
        <div className="color_bar_right">
          <div style={{ height: "100%", width: "20%"}}>-1.0</div>
          <div style={{ height: "100%", width: "20%"}}>-0.6</div>
          <div style={{ height: "100%", width: "20%"}}>-0.2</div>
          <div style={{ height: "100%", width: "20%"}}>0.2</div>
          <div style={{ height: "100%", width: "20%"}}>0.6</div>
          <div style={{ height: "100%", width: "20%"}}>1.0</div>
        </div>
      </div>

      <div style={{ height: "100%", width: "100%" }}>
        <MapContainer center={[-37.8136, 144.9631]} zoom={10} style={{ height: '100vh', width: '100%' }}>
          <SetPane />
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <GeoJSON data={suburbsData} {...geoJsonOptions} />
          {props.attrName!=='' && <CustomMarkers attrName={props.attrName}/>}
        </MapContainer>
      </div>
    </div>
    
    
  );
};

export default SuburbsMap