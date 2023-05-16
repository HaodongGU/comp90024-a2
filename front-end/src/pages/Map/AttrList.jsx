import React from "react";
import 'leaflet/dist/leaflet.css';
import "./Map.scss"



const AttrListItem = (props) => {
  const AnalysisButton = () => {
    return(
      <div className="map_analysis_button_div">
        <h4 className="map_analysis_button">View Analysis</h4>
      </div>
    )
  }

  return (
    <div className="attr_item">
      <div className="attr_btn">
        <input 
          type="radio" 
          name="attr" 
          value={props.attrName}
          onChange={props.handleRadioChange}/> 
        <h4>{props.attrName}</h4>
      </div>
      {props.attrName === props.selectedAttr && <AnalysisButton/>}
    </div>
  )
}


const AttrList = (props) => {
  return (
    <div className="map_left">
      <h3 className="attr_btn"> Impact Factor: </h3>
      <AttrListItem attrName={"Income"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Age"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Crime Rate"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport4"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport5"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport6"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport7"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport8"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport9"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport10"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
      <AttrListItem attrName={"Public Transport11"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange}/>
    </div>
  )
}

export default AttrList