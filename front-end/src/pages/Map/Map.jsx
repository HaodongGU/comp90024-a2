import React, { useState } from "react";
import AttrList from "./AttrList";
import SuburbsMap from "./SuburbsMap";

const Map = () => {
  const [selectedAttr, setSelectedAttr] = useState('');
  const handleRadioChange = (event) => {
    setSelectedAttr(event.target.value);
    console.log("selectedAttr: ", selectedAttr);
  };

  return (
    <div className="map_main">
      <AttrList handleRadioChange={handleRadioChange} selectedAttr={selectedAttr}/>
      <SuburbsMap/>
      {/* <h1 className="attr_btn">hello world</h1> */}
    </div>
  )
}

export default Map