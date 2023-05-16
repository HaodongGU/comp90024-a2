import React, { useState } from "react";
import 'leaflet/dist/leaflet.css';
import "./Map.scss"
import AnalysisChart from "./AnalysisChart";


const AttrListItem = (props) => {
  const AnalysisButton = () => {
    return(
      <div className="map_analysis_button_div" onClick={props.buttonClickHandler}>
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
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const buttonClickHandler = () => {
    setModalIsOpen(true);
    console.log("AttrList buttonClickHandler modalIsOpen: ", modalIsOpen);
  };

  const closeModal = () => {
    setModalIsOpen(false);
    console.log("AttrList closeModal modalIsOpen: ", modalIsOpen);
  };

  return (
    // <div>
      
    //   {/* <AnalysisChart modalIsOpen={modalIsOpen} closeModal={closeModal}/> */}
    // </div>
    <div className="map_left">
      <h3 className="attr_btn"> Impact Factor: </h3>
      <AttrListItem attrName={"Income"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Age"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Public Transport"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Income1"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Income2"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>

      <AnalysisChart modalIsOpen={modalIsOpen} closeModal={closeModal} attrName={props.selectedAttr}/>
    </div>
  )
}

export default AttrList