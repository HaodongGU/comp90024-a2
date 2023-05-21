import React, { useState } from "react";
import 'leaflet/dist/leaflet.css';
import "./Map.scss"
import AnalysisChart from "./AnalysisChart";

const getMarkHint = (attr) => {
  switch (attr){
    case "Income":
      return "HIGH median income";
    case "Age":
      return "HIGH median age";
    default:
      return "DEFAULT MARK VALUE?";
  }
}

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
      {props.selectedAttr !== "" && <p className="map_right_mark_hint">The suburbs with <i>{getMarkHint(props.selectedAttr)}</i> is marked on the map. </p>}
      <AttrListItem attrName={"Income"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Age"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Population"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Crime"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Public Transport"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>
      <AttrListItem attrName={"Sports"} selectedAttr={props.selectedAttr} handleRadioChange={props.handleRadioChange} buttonClickHandler={buttonClickHandler}/>

      <AnalysisChart modalIsOpen={modalIsOpen} closeModal={closeModal} attrName={props.selectedAttr}/>
    </div>
  )
}

export default AttrList