import React, { useState } from "react";
import AttrList from "./AttrList";
import SuburbsMap from "./SuburbsMap";

const Map = () => {
  const [selectedAttr, setSelectedAttr] = useState('');

  const handleRadioChange = (event) => {
    setSelectedAttr(event.target.value);
    console.log("Map selectedAttr: ", selectedAttr);
  };

  return (
    <div className="map_main">
      <AttrList handleRadioChange={handleRadioChange} selectedAttr={selectedAttr}/>
      <SuburbsMap attrName={selectedAttr}/>
      {/* <h1 className="attr_btn">hello world</h1> */}
    </div>
  )
}

export default Map