import React, { useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import suburbsData from './suburbsData.json'; 
import { Icon } from 'leaflet';
import { Marker as LeafletMarker } from 'react-leaflet';
import SadEmoji from "../../static/figure/sadEmoji.png";
import MarkerIncome from "../../static/figure/MarkerIncome.png"


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

  return (
    <LeafletMarker position={props.position} icon={markerIcon} />
  )
};

const CustomMarkers = (props) => {
  const demo = [[-37.8136, 144.9631], [-37.9136, 145.0631], [-38.0136, 145.1631]]
  const positions = demo; //TODO: get request!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  console.log("CustomMarkers positions len: ", positions.length);
  const output = positions.map((position) => (
    <CustomMarker position={position} attrName={props.attrName}/>
  ));
  
  return output;
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
      return '#ff0000'; // red
    }
    //TODO: get request!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return '#ffffff'; // white? trans 
  }

  const geoJsonOptions = {
    style: (feature) => ({
      color: feature.properties.vic_loca_2 === selectedSuburb ? '#ff0000' : '#000000',
      weight: selectedSuburb === feature.properties.vic_loca_2 ? 3 : 1,
      // fillColor: feature.properties.vic_loca_2 === selectedSuburb ? '#ff0000' : '#3388ff',
      fillColor: colorChooser(feature.properties.vic_loca_2, selectedSuburb),
      fillOpacity: 0.2,
    }),
    onEachFeature: (feature, layer) => {
      layer.on({
        click: handleSuburbClick,
      });
    },
  };

  return (
    <MapContainer center={[-37.8136, 144.9631]} zoom={10} style={{ height: '100vh', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <GeoJSON data={suburbsData} {...geoJsonOptions} />
      <CustomMarkers attrName={props.attrName}/>
    </MapContainer>
  );
};

export default SuburbsMap