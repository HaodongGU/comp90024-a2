import React from 'react';
import { GoogleMap, LoadScript, Polygon } from '@react-google-maps/api';
import suburbData from './suburbData.json';
import { passiveSupport } from 'passive-events-support/src/utils'

const containerStyle = {
  width: '100%',
  height: '600px',
};

const center = {
  lat: -35.07228701,
  lng: 141.74552399
};

const options = {
  strokeColor: '#FF0000',
  strokeOpacity: 0.8,
  strokeWeight: 2,
  fillColor: '#FF0000',
  fillOpacity: 0.35,
};

passiveSupport({
  //...
  listeners: [
    {
      element: 'div.some-element',
      event: 'touchstart',
      prevented: true
    }
  ]
})

const MapWithSuburbBoundaries = () => {
  passiveSupport({
    //...
    listeners: [
      {
        element: 'div.some-element',
        event: 'touchstart',
        prevented: true
      }
    ]
  })

  const renderSuburbBoundaries = () => {
    // var output = suburbData.features.map((feature) => (
    //   <Polygon
    //     key={feature.id}
    //     path={feature.geometry.coordinates[0][0].map((coord) => ({
    //       lat: coord[1],
    //       lng: coord[0],
    //     }))}
    //     options={options}
    //   />
    // ));
    // console.log("features size: ", suburbData.features.length);
    // console.log("output size: ", output.length);
    // console.log(suburbData.features[0].geometry.coordinates[0][0][0][0], suburbData.features[0].geometry.coordinates[0][0][0][1])
    
    var output1 = <Polygon 
      key={1}
      path={suburbData.features[0].geometry.coordinates[0][0].map((coord) => ({
        lat: coord[1],
        lng: coord[0],
      }))}
      options={options}
    />
    console.log(output1);
    return output1;
  };

  return (
    <LoadScript googleMapsApiKey="AIzaSyAPcUQ65PDtiTToBTVgXF9uMRTiu5orEyU">
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={10}
      >
        {renderSuburbBoundaries()}
      </GoogleMap>
    </LoadScript>
  );
};

export default MapWithSuburbBoundaries;
