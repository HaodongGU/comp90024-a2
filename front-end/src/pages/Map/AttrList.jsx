import React, { useState } from "react";
import 'leaflet/dist/leaflet.css';
import "./Map.scss"
import AnalysisChart from "./AnalysisChart";
import HappyEmpji from "../../static/figure/happyEmoji.png";
import SadEmoji from "../../static/figure/sadEmoji.png";
import MarkerIncomeBot from "../../static/figure/MarkerIncomeBot.png";
import MarkerIncomeTop from "../../static/figure/MarkerIncomeTop.png";
import MarkerCrimeBot from "../../static/figure/MarkerCrimeBot.png";
import MarkerCrimeTop from "../../static/figure/MarkerCrimeTop.png";
import MarkerAgeBot from "../../static/figure/MarkerAgeBot.png";
import MarkerAgeTop from "../../static/figure/MarkerAgeTop.png";
import MarkerPopulationBot from "../../static/figure/MarkerPopulationBot.png";
import MarkerPopulationTop from "../../static/figure/MarkerPopulationTop.png";
import MarkerTransportBot from "../../static/figure/MarkerTransportBot.png";
import MarkerTransportTop from "../../static/figure/MarkerTransportTop.png";
import MarkerSportsBot from "../../static/figure/MarkerSportsBot.png";
import MarkerSportsTop from "../../static/figure/MarkerSportsTop.png";

const MarkHint = (props) => {
  let word = ''
  let IconBot = null;
  let IconTop = null;
  switch (props.selectedAttr){
    case "Income":
      word = "Median income";
      IconBot = MarkerIncomeBot;
      IconTop = MarkerIncomeTop;
      break;
    case "Age":
      word = "Median age";
      IconBot = MarkerAgeBot;
      IconTop = MarkerAgeTop;
      break;
    case "Population":
      word = "Population density";
      IconBot = MarkerPopulationBot;
      IconTop = MarkerPopulationTop;
      break;
    case "Crime":
      word = "Crime count";
      IconBot = MarkerCrimeBot;
      IconTop = MarkerCrimeTop;
      break;
    case "Public Transport":
      word = "Transport Composite Accessibility Index";
      IconBot = MarkerTransportBot;
      IconTop = MarkerTransportTop;
      break;
    case "Sports":
      word = "Sports facility number";
      IconBot = MarkerSportsBot;
      IconTop = MarkerSportsTop;
      break;
    default:
      word = "DEFAULT MARK VALUE?";
      IconBot = SadEmoji;
      IconTop = HappyEmpji;
      break;
  }
  return (
    <div>
      <div className="hint">
        <p className="map_right_mark_hint"><b>HIGH </b><i>{word}</i>: </p>
        <img src={IconTop} alt="IconTop"/>
      </div>
      <div className="hint">
        <p className="map_right_mark_hint"><b>LOW &nbsp;</b><i>{word}</i>: </p>
        <img src={IconBot} alt="IconBot"/>
      </div>
    </div>
    
  )
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
      {/* {props.selectedAttr !== "" && <p className="map_right_mark_hint">The suburbs with <i>{getMarkHint(props.selectedAttr)}</i> is marked on the map. </p>} */}

      {props.selectedAttr !== "" && <MarkHint selectedAttr={props.selectedAttr}/>}


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